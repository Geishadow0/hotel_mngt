from flask import Flask, render_template, flash, redirect, url_for, session, request, logging
from flask_mysqldb import MySQL
from flask_wtf import Form
from wtforms import StringField, PasswordField, validators
from passlib.hash import sha256_crypt
from functools import wraps
import pdfkit
import os
import random
from flask_mail import Mail, Message


app = Flask(__name__)

#Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hotel'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

#config email 
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'RoyalHotel@hotels.com'
app.config['MAIL_PASSWORD'] = '************'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

#init MYSQL & email
mysql = MySQL(app)
mail = Mail(app)

# Index
@app.route('/')
def index():
    return render_template('main.html')


#ntuk membantu pembuatan form 
class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.Length(min=6, max=150),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


# User Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
   
   #mengambil data
    if request.method=='POST':
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(str(form.password.data))

            # membuatcursor
        cur = mysql.connection.cursor()


        #  query
        cur.execute("INSERT INTO pelanggan(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

        # Commit 
        mysql.connection.commit()

        # menutup koneksi
        cur.close()

        flash('You are now registered and can log in', 'success')

        return redirect(url_for('login'))
    return render_template('register.html', form=form)


#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Form Fields
        username = request.form['username']
        password_candidate = request.form['password']

        # cursor
        cur = mysql.connection.cursor()

        # mengabiluser by username
        result = cur.execute("SELECT * FROM pelanggan WHERE username = %s", [username])


        if result > 0:
            # Get stored hash
            data = cur.fetchone()
            print(data['username'])
            password = data['password']

            # membandingkan Passwords
            if sha256_crypt.verify(request.form['password'], password):
                print("matched and redirecting....")
                # Passed
                #app.logger.info('PASSWORD MATCHED')
                session['logged_in'] = True
                session['username']  = username

                flash('Successfully logged in!', 'success')

                return redirect(url_for('.index'))

            else:
                #username salah
                print("wrong password")
                error = 'Invalid login'
                app.logger.info('PASSWORD DOES NOT MATCH')
                return render_template('login.html', error=error)

            cur.close()
            
        else:
            #username tidak ada
            error = 'Username not found'
            app.logger.info('NO SUCH USER')
            return render_template('login.html', error=error)

    return render_template('login.html')

#untuk membantu memastikan bahwa user telah login
def is_logged_in(f):
    @wraps(f)

    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return (f(*args, **kwargs))
        else:
            flash('Unauthorised access!', 'danger')
            return redirect(url_for('login'))
    return wrap

#logout
@app.route('/logout')
@is_logged_in
def logout():
    #menghaous sesi
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))



    
#booking kamar
@app.route('/rooms/<id>/<price>', methods=['GET', 'POST'])
@is_logged_in
def rooms(id,price):
    #mengambil username dari sesi
    user=session['username']
    #debug print(user)
    cur = mysql.connection.cursor()
    #menyimpan data pada mysql
    cur.execute("INSERT INTO sewa (room_id, pelanggan) VALUES (%s, %s)",(id, user,) )
    cur.execute("INSERT INTO ilog (income) VALUES (%s)",(price,))
    flash('Check in berhasil', 'success')
    session['status']='checked'
    print(id)
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('.index'))

#checkout kamar
@app.route('/checkout', methods=['GET', 'POST'])
@is_logged_in
def checkout():
    #mengambil username
    user=session['username']
    i=1
    cur = mysql.connection.cursor()
    cur.execute("UPDATE sewa SET st=%s WHERE pelanggan=%s",(i,user))
    mysql.connection.commit()
    cur.close()
    flash('Check out berhasil', 'success')
    session.pop('status', None)
    return redirect(url_for('.index'))

#dashboard admin
@app.route('/dashboard', methods=['POST', 'GET'])
@is_logged_in
def dashboard():
    #mengambil data untuk table 
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM ilog")
    ilog = cur.fetchall()
    result2 = cur.execute("SELECT * FROM sewa")
    sewa = cur.fetchall()
    result3 = cur.execute("SELECT * FROM pelanggan")
    user = cur.fetchall()
    if result or result2 or result3> 0:
        return render_template('dashboard.html', ilogs=ilog, sewas=sewa, users=user)
    else:
        flash('No Data available!', 'danger')

    cur.close()
    return render_template('dashboard.html')

#email blast    
@app.route('/sendmail/')
@is_logged_in
def sendmail():
    #email
    msg = Message('Hello', sender = 'RoyalHotel@hotels.com', recipients = ['Administration@hotels.com'])
    msg.body = "Email Sent"
    mail.send(msg)
    flash('Mail Sent!!', 'success')
    return redirect(url_for('/dashboard'))

#htmltopdf 
@app.route('/webprint')
@is_logged_in
def webprint():
    #pdfkit
    pdfkit.from_url('http://127.0.0.1:5000/dashboard', 'print.pdf')
    
#aout page    
@app.route('/about')
def about():
    return render_template('about.html')
    
        
    
if __name__ == '__main__':
    SECRET_KEY = os.urandom(32)
    app.config['SECRET_KEY'] = SECRET_KEY

    print(SECRET_KEY)

    SECRET_KEY = os.urandom(32)
    app.config['WTF_CSRF_SECRET_KEY']=SECRET_KEY

    app.run(debug = True)
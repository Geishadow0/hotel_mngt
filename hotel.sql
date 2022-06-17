-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 17, 2022 at 07:16 AM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `hotel`
--

-- --------------------------------------------------------

--
-- Table structure for table `ilog`
--

CREATE TABLE `ilog` (
  `id` int(11) NOT NULL,
  `income` int(11) NOT NULL,
  `time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `ilog`
--

INSERT INTO `ilog` (`id`, `income`, `time`) VALUES
(4, 200, '2022-06-16 13:07:59');

-- --------------------------------------------------------

--
-- Table structure for table `kamar`
--

CREATE TABLE `kamar` (
  `id` int(11) NOT NULL,
  `nama_kamar` varchar(100) NOT NULL,
  `harga` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kamar`
--

INSERT INTO `kamar` (`id`, `nama_kamar`, `harga`) VALUES
(1, 'Standard Single', 150),
(2, 'Standard Double', 200),
(3, 'Premium Single', 300),
(4, 'Premium Double', 350),
(5, 'Presidential Suites', 400);

-- --------------------------------------------------------

--
-- Table structure for table `pelanggan`
--

CREATE TABLE `pelanggan` (
  `id` int(11) NOT NULL,
  `username` varchar(100) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(100) NOT NULL,
  `date` datetime NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `pelanggan`
--

INSERT INTO `pelanggan` (`id`, `username`, `name`, `email`, `password`, `date`) VALUES
(1, 'admin', 'admin', 'admin@mail.com', '$5$rounds=535000$hrI9JNDp3SVQX52r$eXGX.1LCbRywB92BAHm50OzsmXyq8bMrA9ZI2/Ib4n9', '2022-06-16 00:00:00'),
(2, 'pass', 'pass', 'pass@mail.com', '$5$rounds=535000$I03iQ7q8Gburp18Z$emN.Ir/O.ALY.9QR/DHLFn9EnAp85qE3vBQtP8ixdt0', '2022-06-16 00:00:00');

-- --------------------------------------------------------

--
-- Table structure for table `sewa`
--

CREATE TABLE `sewa` (
  `id` int(11) NOT NULL,
  `pelanggan` varchar(100) NOT NULL,
  `room_id` int(11) NOT NULL,
  `check_in` timestamp NOT NULL DEFAULT current_timestamp(),
  `check_out` timestamp NULL DEFAULT NULL ON UPDATE current_timestamp(),
  `st` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sewa`
--

INSERT INTO `sewa` (`id`, `pelanggan`, `room_id`, `check_in`, `check_out`, `st`) VALUES
(1, 'admin', 3, '2022-06-16 12:26:00', '2022-06-16 13:08:04', 1),
(2, 'admin', 4, '2022-06-16 12:26:11', '2022-06-16 13:08:04', 1),
(3, 'admin', 2, '2022-06-16 12:27:57', '2022-06-16 13:08:04', 1),
(5, 'admin', 1, '2022-06-16 12:33:26', '2022-06-16 13:08:04', 1),
(7, 'admin', 2, '2022-06-16 12:34:18', '2022-06-16 13:08:04', 1),
(8, 'admin', 5, '2022-06-16 12:34:33', '2022-06-16 13:08:04', 1),
(9, 'admin', 2, '2022-06-16 13:07:59', '2022-06-16 13:08:04', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `ilog`
--
ALTER TABLE `ilog`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `kamar`
--
ALTER TABLE `kamar`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pelanggan`
--
ALTER TABLE `pelanggan`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indexes for table `sewa`
--
ALTER TABLE `sewa`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `ilog`
--
ALTER TABLE `ilog`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `kamar`
--
ALTER TABLE `kamar`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `pelanggan`
--
ALTER TABLE `pelanggan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `sewa`
--
ALTER TABLE `sewa`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

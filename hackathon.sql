-- phpMyAdmin SQL Dump
-- version 4.7.1
-- https://www.phpmyadmin.net/
--
-- Host: sql6.freemysqlhosting.net
-- Generation Time: Jul 19, 2021 at 12:41 PM
-- Server version: 5.5.62-0ubuntu0.14.04.1
-- PHP Version: 7.0.33-0ubuntu0.16.04.16

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `sql6426420`
--

-- --------------------------------------------------------

--
-- Table structure for table `doctor`
--

CREATE TABLE `doctor` (
  `did` varchar(15) NOT NULL,
  `name` varchar(40) NOT NULL,
  `email` varchar(30) NOT NULL,
  `password` varchar(40) NOT NULL,
  `phone` int(11) NOT NULL,
  `special` varchar(30) NOT NULL,
  `degree` varchar(30) NOT NULL,
  `gender` varchar(7) NOT NULL,
  `location` varchar(50) NOT NULL,
  `startm` time NOT NULL DEFAULT '08:00:00',
  `endm` time NOT NULL DEFAULT '11:00:00',
  `starte` time NOT NULL DEFAULT '14:00:00',
  `ende` time NOT NULL DEFAULT '20:00:00',
  `ratings` float NOT NULL DEFAULT '5'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `doctor`
--

INSERT INTO `doctor` (`did`, `name`, `email`, `password`, `phone`, `special`, `degree`, `gender`, `location`, `startm`, `endm`, `starte`, `ende`, `ratings`) VALUES
('DOC79bb6b2a0b', 'Tejaswi Kumar', 'tejpatna@gmail.com', '698396d4a59541364832', 2147483647, 'GENERAL PHYSICIAN', 'MBBS', 'Male', 'PATNA', '08:00:00', '11:00:00', '14:00:00', '20:00:00', 5);

-- --------------------------------------------------------

--
-- Table structure for table `event`
--

CREATE TABLE `event` (
  `id` int(10) UNSIGNED NOT NULL,
  `title` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `class` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `start_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `end_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `pid` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `did` varchar(15) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pname` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `dname` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `event`
--

INSERT INTO `event` (`id`, `title`, `url`, `class`, `start_date`, `end_date`, `pid`, `did`, `pname`, `dname`) VALUES
(1, 'Meeting', 'https://docit-videocall.herokuapp.com/PAT379939adc4DOC79bb6b2a0b', 'event', '2021-07-01 14:00:00', '2021-07-01 14:00:00', 'PAT379939adc4', 'DOC79bb6b2a0b', 'Tejaswi Kumar', 'Tejaswi Kumar');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `pid` varchar(15) NOT NULL,
  `name` varchar(40) NOT NULL,
  `email` varchar(40) NOT NULL,
  `psw` varchar(20) NOT NULL,
  `phone` int(11) NOT NULL,
  `gender` varchar(7) NOT NULL,
  `date` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`pid`, `name`, `email`, `psw`, `phone`, `gender`, `date`) VALUES
('PAT379939adc4', 'Tejaswi Kumar', 'tejpatna24@gmail.com', 'test123', 2147483647, 'Male', '2021-07-14');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

-- phpMyAdmin SQL Dump
-- version 5.1.2
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: May 28, 2025 at 02:08 PM
-- Server version: 5.7.24
-- PHP Version: 8.3.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ferreira_guilherme_deva1a_notes_2025`
--
CREATE DATABASE IF NOT EXISTS `ferreira_guilherme_deva1a_notes_2025` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `ferreira_guilherme_deva1a_notes_2025`;

-- --------------------------------------------------------

--
-- Table structure for table `adresses`
--

DROP TABLE IF EXISTS `adresses`;
CREATE TABLE `adresses` (
  `id_adresse` int(11) NOT NULL,
  `ville` varchar(32) DEFAULT NULL,
  `rue` varchar(64) DEFAULT NULL,
  `nip` int(11) DEFAULT NULL,
  `pays` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `adresses`
--

INSERT INTO `adresses` (`id_adresse`, `ville`, `rue`, `nip`, `pays`) VALUES
(1, 'Wherever', 'ThisStreetIs', 404, 'WeDontKnow'),
(3, 'freg', 'fgdfg', 45, 'regd'),
(4, 'a', 'a', 2341, 'a');

-- --------------------------------------------------------

--
-- Table structure for table `apprentis`
--

DROP TABLE IF EXISTS `apprentis`;
CREATE TABLE `apprentis` (
  `id_apprenti` int(11) NOT NULL,
  `annee_scolaire` int(11) DEFAULT NULL,
  `id_adresse` int(11) DEFAULT NULL,
  `id_formateur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `apprentis`
--

INSERT INTO `apprentis` (`id_apprenti`, `annee_scolaire`, `id_adresse`, `id_formateur`) VALUES
(3, 2, 3, 1),
(4, 1, 4, 1);

-- --------------------------------------------------------

--
-- Table structure for table `branches`
--

DROP TABLE IF EXISTS `branches`;
CREATE TABLE `branches` (
  `id_branche` int(11) NOT NULL,
  `nom` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `branches`
--

INSERT INTO `branches` (`id_branche`, `nom`) VALUES
(1005, 'bababa'),
(1006, 'afsg'),
(1007, 'dfgdfgre'),
(1008, 'fsf'),
(1009, 'asdg'),
(1010, 'fs');

-- --------------------------------------------------------

--
-- Table structure for table `bureaux`
--

DROP TABLE IF EXISTS `bureaux`;
CREATE TABLE `bureaux` (
  `id_bureau` int(11) NOT NULL,
  `nom` varchar(32) DEFAULT NULL,
  `id_formateur` int(11) DEFAULT NULL,
  `id_apprenti` int(11) DEFAULT NULL,
  `id_adresse` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- Table structure for table `formateurs`
--

DROP TABLE IF EXISTS `formateurs`;
CREATE TABLE `formateurs` (
  `id_formateur` int(11) NOT NULL,
  `id_adresse` int(11) DEFAULT NULL,
  `id_personne` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `formateurs`
--

INSERT INTO `formateurs` (`id_formateur`, `id_adresse`, `id_personne`) VALUES
(1, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
CREATE TABLE `notes` (
  `id_note` int(11) NOT NULL,
  `valeur` decimal(2,1) DEFAULT NULL,
  `id_apprenti` int(11) DEFAULT NULL,
  `id_semestre` int(11) DEFAULT NULL,
  `id_branche` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `notes`
--

INSERT INTO `notes` (`id_note`, `valeur`, `id_apprenti`, `id_semestre`, `id_branche`) VALUES
(1, '2.0', 3, 5, 1005);

-- --------------------------------------------------------

--
-- Table structure for table `personnes`
--

DROP TABLE IF EXISTS `personnes`;
CREATE TABLE `personnes` (
  `id_personne` int(11) NOT NULL,
  `prenom` varchar(32) DEFAULT NULL,
  `nom` varchar(32) DEFAULT NULL,
  `mail` varchar(64) DEFAULT NULL,
  `sexe` char(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `personnes`
--

INSERT INTO `personnes` (`id_personne`, `prenom`, `nom`, `mail`, `sexe`) VALUES
(1, 'Arthur', 'Verdon', 'arthur.verdon@gmail.com', 'M'),
(3, 'grs', 'gfdg', 'guilherme.ferreira@gmail.com', 'M'),
(4, 'a', 'a', 'a@g', 'M');

-- --------------------------------------------------------

--
-- Table structure for table `semestres`
--

DROP TABLE IF EXISTS `semestres`;
CREATE TABLE `semestres` (
  `id_semestre` int(11) NOT NULL,
  `valeur` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `semestres`
--

INSERT INTO `semestres` (`id_semestre`, `valeur`) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `adresses`
--
ALTER TABLE `adresses`
  ADD PRIMARY KEY (`id_adresse`);

--
-- Indexes for table `apprentis`
--
ALTER TABLE `apprentis`
  ADD PRIMARY KEY (`id_apprenti`),
  ADD KEY `id_adresse` (`id_adresse`),
  ADD KEY `id_formateur` (`id_formateur`);

--
-- Indexes for table `branches`
--
ALTER TABLE `branches`
  ADD PRIMARY KEY (`id_branche`);

--
-- Indexes for table `bureaux`
--
ALTER TABLE `bureaux`
  ADD PRIMARY KEY (`id_bureau`),
  ADD KEY `id_formateur` (`id_formateur`),
  ADD KEY `id_apprenti` (`id_apprenti`),
  ADD KEY `id_adresse` (`id_adresse`);

--
-- Indexes for table `formateurs`
--
ALTER TABLE `formateurs`
  ADD PRIMARY KEY (`id_formateur`),
  ADD KEY `id_personne` (`id_personne`),
  ADD KEY `id_adresse` (`id_adresse`);

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id_note`),
  ADD KEY `id_apprenti` (`id_apprenti`),
  ADD KEY `id_semestre` (`id_semestre`),
  ADD KEY `id_branche` (`id_branche`);

--
-- Indexes for table `personnes`
--
ALTER TABLE `personnes`
  ADD PRIMARY KEY (`id_personne`);

--
-- Indexes for table `semestres`
--
ALTER TABLE `semestres`
  ADD PRIMARY KEY (`id_semestre`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `adresses`
--
ALTER TABLE `adresses`
  MODIFY `id_adresse` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `branches`
--
ALTER TABLE `branches`
  MODIFY `id_branche` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1011;

--
-- AUTO_INCREMENT for table `bureaux`
--
ALTER TABLE `bureaux`
  MODIFY `id_bureau` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `formateurs`
--
ALTER TABLE `formateurs`
  MODIFY `id_formateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id_note` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `personnes`
--
ALTER TABLE `personnes`
  MODIFY `id_personne` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `semestres`
--
ALTER TABLE `semestres`
  MODIFY `id_semestre` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `apprentis`
--
ALTER TABLE `apprentis`
  ADD CONSTRAINT `apprentis_ibfk_1` FOREIGN KEY (`id_adresse`) REFERENCES `adresses` (`id_adresse`),
  ADD CONSTRAINT `apprentis_ibfk_2` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`);

--
-- Constraints for table `bureaux`
--
ALTER TABLE `bureaux`
  ADD CONSTRAINT `bureaux_ibfk_1` FOREIGN KEY (`id_formateur`) REFERENCES `formateurs` (`id_formateur`),
  ADD CONSTRAINT `bureaux_ibfk_2` FOREIGN KEY (`id_apprenti`) REFERENCES `apprentis` (`id_apprenti`),
  ADD CONSTRAINT `bureaux_ibfk_3` FOREIGN KEY (`id_adresse`) REFERENCES `adresses` (`id_adresse`);

--
-- Constraints for table `formateurs`
--
ALTER TABLE `formateurs`
  ADD CONSTRAINT `formateurs_ibfk_1` FOREIGN KEY (`id_personne`) REFERENCES `personnes` (`id_personne`),
  ADD CONSTRAINT `formateurs_ibfk_2` FOREIGN KEY (`id_adresse`) REFERENCES `adresses` (`id_adresse`);

--
-- Constraints for table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`id_apprenti`) REFERENCES `apprentis` (`id_apprenti`),
  ADD CONSTRAINT `notes_ibfk_2` FOREIGN KEY (`id_semestre`) REFERENCES `semestres` (`id_semestre`),
  ADD CONSTRAINT `notes_ibfk_3` FOREIGN KEY (`id_branche`) REFERENCES `branches` (`id_branche`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

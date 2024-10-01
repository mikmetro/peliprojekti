-- --------------------------------------------------------
-- Verkkotietokone:              127.0.0.1
-- Palvelinversio:               10.9.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Versio:              11.3.0.6295
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

DROP TABLE IF EXISTS `kentta_inventaario`;
CREATE TABLE IF NOT EXISTS `kentta_inventaario` (
	`id` int(11) NOT NULL,
	`kentan_id` int(11) NOT NULL,
	`pelaaja_id` int(11) NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`kentan_id`) REFERENCES airport(`id`),
	FOREIGN KEY (`pelaaja_id`) REFERENCES pelaaja(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `pelin_lentokentat`;
CREATE TABLE IF NOT EXISTS `pelaaja` (
	`id` int(11) NOT NULL,
	`lokaatio` varchar(40) DEFAULT NULL,
	`hinta` float(11) DEFAULT NULL,
	`tuotto` float(11) DEFAULT NULL,
	`kuvaus` varchar(100) DEFAULT NULL,
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tapahtuma_litos`;
CREATE TABLE IF NOT EXISTS `tapahtuma_litos` (
	`tapahtuma_id` int(11) NOT NULL,
	`inventaario_id` int(11) NOT NULL
	FOREIGN KEY (`tapahtuma_id`) REFERENCES tapahtuma(`id`)
	FOREIGN KEY (`inventaario_id`) REFERENCES kentta_inventaario(`id`)

) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `tapahtuma`;
CREATE TABLE IF NOT EXISTS `tapahtuma` (
	`id` int(11) NOT NULL,
	`kuvaus` varchar(100) DEFAULT NULL,
	`vaikutus` varchar(100) DEFAULT NULL,
	`todennäkoisyys` int(11),
	PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping structure for taulu flight_game.airport
DROP TABLE IF EXISTS `airport`;
CREATE TABLE IF NOT EXISTS `airport` (
  `id` int(11) NOT NULL,
  `ident` varchar(40) NOT NULL,
  `type` varchar(40) DEFAULT NULL,
  `name` varchar(40) DEFAULT NULL,
  `latitude_deg` double DEFAULT NULL,
  `longitude_deg` double DEFAULT NULL,
  `elevation_ft` int(11) DEFAULT NULL,
  `continent` varchar(40) DEFAULT NULL,
  `iso_country` varchar(40) DEFAULT NULL,
  `iso_region` varchar(40) DEFAULT NULL,
  `municipality` varchar(40) DEFAULT NULL,
  `scheduled_service` varchar(40) DEFAULT NULL,
  `gps_code` varchar(40) DEFAULT NULL,
  `iata_code` varchar(40) DEFAULT NULL,
  `local_code` varchar(40) DEFAULT NULL,
  `home_link` varchar(40) DEFAULT NULL,
  `wikipedia_link` varchar(40) DEFAULT NULL,
  `keywords` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`ident`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping structure for taulu flight_game.country
DROP TABLE IF EXISTS `country`;
CREATE TABLE IF NOT EXISTS `country` (
  `iso_country` varchar(40) NOT NULL,
  `name` varchar(40) DEFAULT NULL,
  `continent` varchar(40) DEFAULT NULL,
  `wikipedia_link` varchar(40) DEFAULT NULL,
  `keywords` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`iso_country`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

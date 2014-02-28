-- Server version	5.1.63-log

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `savingxfun$savings`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `savingxfun$savings` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `savingxfun$savings`;

--
-- Table structure for table `customers`
--

DROP TABLE IF EXISTS `customers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `customers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` text,
  `address` text,
  `cellno` text,
  `email` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customers`
--

LOCK TABLES `customers` WRITE;
/*!40000 ALTER TABLE `customers` DISABLE KEYS */;
INSERT INTO `customers` VALUES (1,'Marvin','Cebu','23423','admin@admin.com'),(2,'Matt','Cebu','94030','admin@admin.com'),(3,'dino','Cebu','83738','admin@admin3.com');
/*!40000 ALTER TABLE `customers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `loans` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customerid` int(11) DEFAULT NULL,
  `date_rel` text,
  `date_due` text,
  `amount` double DEFAULT NULL,
  `interest` double DEFAULT NULL,
  `total_payable` double DEFAULT NULL,
  `total_payment` double DEFAULT NULL,
  `outstanding_bal` double DEFAULT NULL,
  `fully_paidon` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
INSERT INTO `loans` VALUES (3,1,'02-13-2014','02-13-2014',6000,7,6420,2000,4420,'02-13-2014'),(4,3,'02-13-2014','02-13-2014',3000,6,3180,1000,2180,'02-22-2014'),(5,2,'02-14-2014','02-28-2014',10000,5,10700,4.03,10699,'02-28-2014'),(6,3,'02-18-2014','02-18-2014',20000,5,21000,5000,16000,'02-18-2014'),(7,3,'02-18-2014','02-18-2014',10000,5,10500,3000,7500,'02-18-2014'),(8,3,'02-18-2014','02-18-2014',1000,5,1050,1000,50,'02-18-2014');
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `users` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(80) NOT NULL,
  `pwd` char(40) NOT NULL,
  `email` varchar(100) NOT NULL,
  `privilege` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'admin','5b378bb184b10bf80515942427422f0168ac8020','mattbrnrdc@gmail.com',1),(2,'marzim','5b378bb184b10bf80515942427422f0168ac8020','admin@admin.com',1),(3,'matt','5b378bb184b10bf80515942427422f0168ac8020','mattbrnrdc@gmail.com',0),(4,'matt2','969a2b03bd6793d92869f0c7c6e51f79ff0cb2f6','mattbrnrdc@gmail.com',0),(5,'admin1','969a2b03bd6793d92869f0c7c6e51f79ff0cb2f6','admin@admin.com',0),(6,'admin2','969a2b03bd6793d92869f0c7c6e51f79ff0cb2f6','admin@admin.com',0),(7,'admin3','969a2b03bd6793d92869f0c7c6e51f79ff0cb2f6','admin@admin.com',0);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-02-26 15:32:32

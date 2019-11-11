-- MySQL dump 10.13  Distrib 5.7.27, for Linux (x86_64)
--
-- Host: localhost    Database: travelcombot
-- ------------------------------------------------------
-- Server version	5.7.27-0ubuntu0.18.04.1

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
-- Table structure for table `community`
--

DROP TABLE IF EXISTS `community`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `community` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `url` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `community`
--

LOCK TABLES `community` WRITE;
/*!40000 ALTER TABLE `community` DISABLE KEYS */;
INSERT INTO `community` VALUES (1,'Смена','https://todo.com/','Описание...'),(2,'Сансерферы','https://todo.com/','Описание...');
/*!40000 ALTER TABLE `community` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `country`
--

DROP TABLE IF EXISTS `country`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `country` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `country`
--

LOCK TABLES `country` WRITE;
/*!40000 ALTER TABLE `country` DISABLE KEYS */;
INSERT INTO `country` VALUES (1,'Тайланд'),(2,'Индия'),(3,'Грузия'),(4,'Марокко'),(5,'Шри-Ланка'),(6,'Турция'),(7,'Албания'),(8,'Вьетнам'),(9,'Филиппины'),(10,'Непал'),(11,'Индонезия'),(12,'Мексика'),(13,'Малайзия');
/*!40000 ALTER TABLE `country` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event`
--

DROP TABLE IF EXISTS `event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` int(11) NOT NULL,
  `date_of_the_event` date NOT NULL,
  `type_of_event` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_event__country` (`country`),
  KEY `idx_event__type_of_event` (`type_of_event`),
  CONSTRAINT `fk_event__country` FOREIGN KEY (`country`) REFERENCES `country` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_event__type_of_event` FOREIGN KEY (`type_of_event`) REFERENCES `typeofevent` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event`
--

LOCK TABLES `event` WRITE;
/*!40000 ALTER TABLE `event` DISABLE KEYS */;
INSERT INTO `event` VALUES (1,5,'2019-05-01',1,'Sun Gathering 11.0'),(2,12,'2018-04-01',1,'Sun Gathering 10.0'),(3,6,'2017-10-01',1,'Sun Gathering 9.0'),(4,4,'2017-05-01',1,'Sun Gathering 8.0'),(5,10,'2016-10-01',1,'Sun Gathering 7.0'),(6,11,'2016-04-01',1,'Sun Gathering 6.0'),(7,3,'2015-09-01',1,'Sun Gathering 5.0'),(8,9,'2015-04-01',1,'Sun Gathering 4.0'),(9,8,'2014-11-01',1,'Sun Gathering 3.0'),(10,2,'2014-04-01',1,'Sun Gathering 2.0'),(11,1,'2013-11-01',1,'Sun Gathering 1.0'),(12,7,'2019-08-01',2,'Университет 5.0'),(13,1,'2018-10-01',2,'Университет 4.0'),(14,6,'2017-09-01',2,'Университет 3.0'),(15,5,'2017-03-01',2,'Университет 2.0'),(16,2,'2016-02-01',2,'Университет 1.0'),(17,3,'2019-08-01',3,'Йога-ретрит 2.0'),(18,2,'2017-01-01',3,'Йога-ретрит 1.0'),(19,6,'2019-10-01',4,'СанАториум 2.0'),(20,1,'2018-10-01',4,'СанАториум 1.0'),(21,3,'2019-08-01',5,'SunWomanCamp 2.0'),(22,3,'2019-06-01',5,'SunWomanCamp 1.0'),(23,13,'2016-03-01',1,'Sunsurfers Masala');
/*!40000 ALTER TABLE `event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `event_user`
--

DROP TABLE IF EXISTS `event_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `event_user` (
  `event` int(11) NOT NULL,
  `user` int(11) NOT NULL,
  PRIMARY KEY (`event`,`user`),
  KEY `idx_event_user` (`user`),
  CONSTRAINT `fk_event_user__event` FOREIGN KEY (`event`) REFERENCES `event` (`id`),
  CONSTRAINT `fk_event_user__user` FOREIGN KEY (`user`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `event_user`
--

LOCK TABLES `event_user` WRITE;
/*!40000 ALTER TABLE `event_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `event_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `typeofevent`
--

DROP TABLE IF EXISTS `typeofevent`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `typeofevent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `community` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_typeofevent__community` (`community`),
  CONSTRAINT `fk_typeofevent__community` FOREIGN KEY (`community`) REFERENCES `community` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `typeofevent`
--

LOCK TABLES `typeofevent` WRITE;
/*!40000 ALTER TABLE `typeofevent` DISABLE KEYS */;
INSERT INTO `typeofevent` VALUES (1,'Санслёт',2),(2,'Университет',2),(3,'Йога-ретрит',2),(4,'СанАториум',2),(5,'SunWomanCamp',2),(6,'Smena station',2);
/*!40000 ALTER TABLE `typeofevent` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `photo` varchar(255) NOT NULL,
  `is_host` tinyint(1) NOT NULL,
  `about` longtext,
  `telegram` varchar(255) NOT NULL,
  `insta` varchar(255) DEFAULT NULL,
  `community` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user__community` (`community`),
  CONSTRAINT `fk_user__community` FOREIGN KEY (`community`) REFERENCES `community` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `visited_paces`
--

DROP TABLE IF EXISTS `visited_paces`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `visited_paces` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user` int(11) NOT NULL,
  `coordinates` varchar(255) NOT NULL,
  `city` varchar(255) NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_visited_paces__user` (`user`),
  CONSTRAINT `fk_visited_paces__user` FOREIGN KEY (`user`) REFERENCES `user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `visited_paces`
--

LOCK TABLES `visited_paces` WRITE;
/*!40000 ALTER TABLE `visited_paces` DISABLE KEYS */;
/*!40000 ALTER TABLE `visited_paces` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-10-02 18:21:14

CREATE TABLE whitelist (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `username` varchar(255),
  `phone` varchar(255),
  PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

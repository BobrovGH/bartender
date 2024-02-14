-- MySQL dump 10.13  Distrib 8.0.34, for macos13 (arm64)
--
-- Host: localhost    Database: bartender
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `items` (
  `item_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `volume` decimal(10,2) DEFAULT NULL,
  `alcohol` decimal(5,2) DEFAULT NULL,
  `year` int DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `country` varchar(255) DEFAULT NULL,
  `producer` varchar(255) DEFAULT NULL,
  `empty_weight` decimal(10,2) DEFAULT NULL,
  `about` text,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'Absolutо','Водка',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(2,'Прусский стандарт','Водка',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(3,'БаКарпи','Ром',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(5,'Алладин','Джин',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(7,'Коза','Светлое пиво',0.50,5.00,NULL,NULL,NULL,NULL,NULL,NULL),(8,'Absolutо','Водка',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(9,'Прусский стандарт','Водка',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(11,'АльПака','Текила',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(12,'Алладин','Джин',0.70,40.00,NULL,NULL,NULL,NULL,NULL,NULL),(13,'Коза','Тёмное пиво',0.50,5.00,NULL,NULL,NULL,NULL,NULL,NULL),(14,'Коза','Светлое пиво',0.50,5.00,NULL,NULL,NULL,NULL,NULL,NULL);
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-14  4:49:03

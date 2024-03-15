-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (arm64)
--
-- Host: localhost    Database: travel_project
-- ------------------------------------------------------
-- Server version	8.3.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `accommodations`
--

DROP TABLE IF EXISTS `accommodations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `accommodations` (
  `hotelid` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `location` varchar(255) NOT NULL,
  `price` varchar(255) NOT NULL,
  `amenities` text,
  `rating` int DEFAULT NULL,
  PRIMARY KEY (`hotelid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `accommodations`
--

LOCK TABLES `accommodations` WRITE;
/*!40000 ALTER TABLE `accommodations` DISABLE KEYS */;
INSERT INTO `accommodations` VALUES (1,'The Plaza','Manhattan','Luxury','Wi-Fi, Pool, Spa',5),(2,'Waldorf Astoria','Manhattan','Luxury','Wi-Fi, Pool, Restaurant',5),(3,'The NoMad Hotel','Manhattan','Mid-range','Wi-Fi, Restaurant, Bar',4),(4,'Pod 51','Midtown East','Budget','Wi-Fi, Cafe',3),(5,'YOTEL New York','Hell\'s Kitchen','Mid-range','Wi-Fi, Terrace',4),(6,'Hotel Pennsylvania','Midtown','Budget','Wi-Fi, Restaurant',2),(7,'The Jane','West Village','Budget','Wi-Fi, Bar',3),(8,'The Bowery Hotel','Lower East Side','Luxury','Wi-Fi, Restaurant, Bar',5),(9,'Ace Hotel New York','Flatiron District','Mid-range','Wi-Fi, Bar, Cafe',4),(10,'The Mercer','SoHo','Luxury','Wi-Fi, Restaurant, Bar',5);
/*!40000 ALTER TABLE `accommodations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `local_transport`
--

DROP TABLE IF EXISTS `local_transport`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `local_transport` (
  `transportid` int NOT NULL,
  `type` varchar(255) DEFAULT NULL,
  `route_name` varchar(255) DEFAULT NULL,
  `operating_hours` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`transportid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `local_transport`
--

LOCK TABLES `local_transport` WRITE;
/*!40000 ALTER TABLE `local_transport` DISABLE KEYS */;
INSERT INTO `local_transport` VALUES (1,'Subway','All lines','2.75',24.00),(2,'Bus','Multiple','2.75',5.00),(3,'Taxi','Any','Metered',24.00),(4,'Bike Rental','Any','10',24.00),(5,'Subway','All lines','2.75',24.00),(6,'Bus','Multiple','2.75',5.00),(7,'Taxi','Any','Metered',24.00),(8,'Bike Rental','Any','10',24.00),(9,'Subway','All lines','2.75',24.00),(10,'Bus','Multiple','2.75',5.00);
/*!40000 ALTER TABLE `local_transport` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `points_of_interest`
--

DROP TABLE IF EXISTS `points_of_interest`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `points_of_interest` (
  `pointid` int NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `location` varchar(255) DEFAULT NULL,
  `description` text,
  `type` varchar(255) DEFAULT NULL,
  `recommended_visit_duration` varchar(255) DEFAULT NULL,
  `hotelid` int DEFAULT NULL,
  PRIMARY KEY (`pointid`),
  KEY `fk_accommodations` (`hotelid`),
  CONSTRAINT `fk_accommodations` FOREIGN KEY (`hotelid`) REFERENCES `accommodations` (`hotelid`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `points_of_interest`
--

LOCK TABLES `points_of_interest` WRITE;
/*!40000 ALTER TABLE `points_of_interest` DISABLE KEYS */;
INSERT INTO `points_of_interest` VALUES (1,'Statue of Liberty','Liberty Island','Landmark','18.5','9:00-16:00',NULL),(2,'Central Park','Manhattan','Park','0.0','6:00-1:00',1),(3,'Empire State Building','Manhattan','Landmark','42.0','8:00-2:00',1),(4,'Times Square','Manhattan','Landmark','0.0','Open 24 hours',1),(5,'Brooklyn Bridge','New York','Landmark','0.0','Open 24 hours',NULL),(6,'Broadway Theaters','Manhattan','Entertainment','75.0','Varies',1),(7,'The Metropolitan Museum of Art','Manhattan','Museum','25.0','10:00-17:00',1),(8,'9/11 Memorial','Manhattan','Memorial','26.0','7:30-21:00',1),(9,'High Line','Manhattan','Park','0.0','7:00-22:00',1),(10,'One World Observatory','Manhattan','Observatory','35.0','8:00-20:00',1);
/*!40000 ALTER TABLE `points_of_interest` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `transport_options`
--

DROP TABLE IF EXISTS `transport_options`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `transport_options` (
  `transportid` int NOT NULL,
  `mode_of_transport` varchar(255) DEFAULT NULL,
  `provider` varchar(255) DEFAULT NULL,
  `departure_time` datetime DEFAULT NULL,
  `duration` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `destination` varchar(255) DEFAULT 'New York',
  `origin` varchar(255) DEFAULT 'Boston',
  PRIMARY KEY (`transportid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `transport_options`
--

LOCK TABLES `transport_options` WRITE;
/*!40000 ALTER TABLE `transport_options` DISABLE KEYS */;
INSERT INTO `transport_options` VALUES (1,'Bus','Greyhound','2024-03-15 08:00:00','4 hours',25.00,'New York','Boston'),(2,'Train','Amtrak','2024-03-15 09:00:00','3.5 hours',40.00,'New York','Boston'),(3,'Flight','Delta Airlines','2024-03-15 07:00:00','1.5 hours',150.00,'New York','Boston'),(4,'Car Rental','Enterprise','0000-00-00 00:00:00','Variable',65.00,'New York','Boston'),(5,'Bus','Megabus','2024-03-15 10:00:00','4.5 hours',20.00,'New York','Boston'),(6,'Train','Amtrak','2024-03-15 11:00:00','3 hours',45.00,'New York','Boston'),(7,'Flight','United Airlines','2024-03-15 06:00:00','1 hour',120.00,'New York','Boston'),(8,'Car Rental','Hertz','0000-00-00 00:00:00','Variable',70.00,'New York','Boston'),(9,'Bus','BoltBus','2024-03-15 12:00:00','4 hours',22.00,'New York','Boston'),(10,'Train','Amtrak','2024-03-15 13:00:00','3.5 hours',40.00,'New York','Boston');
/*!40000 ALTER TABLE `transport_options` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-03-14 21:42:32

-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: mydb
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `angajati`
--

DROP TABLE IF EXISTS `angajati`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `angajati` (
  `AngajatID` int NOT NULL AUTO_INCREMENT,
  `Nume` varchar(45) NOT NULL,
  `Prenume` varchar(45) NOT NULL,
  `DepartamentID` int DEFAULT NULL,
  `Nr_telefon` varchar(45) NOT NULL,
  `Email` varchar(45) NOT NULL,
  `CNP` varchar(45) NOT NULL,
  `Data_nasterii` date NOT NULL,
  `Oras` varchar(45) NOT NULL,
  `Salariu` char(10) CHARACTER SET utf8mb3 COLLATE utf8mb3_general_ci DEFAULT NULL,
  PRIMARY KEY (`AngajatID`),
  UNIQUE KEY `CNP_UNIQUE` (`CNP`),
  UNIQUE KEY `Nr_telefon_UNIQUE` (`Nr_telefon`),
  KEY `fk_A_D_idx` (`DepartamentID`),
  CONSTRAINT `fk_A_D` FOREIGN KEY (`DepartamentID`) REFERENCES `departamente` (`DepartamentID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `angajati`
--

LOCK TABLES `angajati` WRITE;
/*!40000 ALTER TABLE `angajati` DISABLE KEYS */;
INSERT INTO `angajati` VALUES (1,'Albu','Cristian',2,'0770234998','albu_cristian','5030405199967','2003-04-05','Costanta','4000'),(2,'Petrescu','Claudia',3,'0761660989','petrescu_claudia@yahoo.com','6020109667456','2002-01-09','Constanta','4200'),(3,'Baidoc','Lorena',1,'0770213990','baidoc_lorena@yahoo.com','6020105556391','2002-01-20','Bucuresti','5000'),(4,'Grigorescu','Vlad',4,'0760225699','grigo_vlad@yahoo.com','5010701234552','2001-07-01','Bucuresti','4100');
/*!40000 ALTER TABLE `angajati` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categorii`
--

DROP TABLE IF EXISTS `categorii`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categorii` (
  `CategorieID` int NOT NULL AUTO_INCREMENT,
  `Denumire` varchar(45) NOT NULL,
  PRIMARY KEY (`CategorieID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categorii`
--

LOCK TABLES `categorii` WRITE;
/*!40000 ALTER TABLE `categorii` DISABLE KEYS */;
INSERT INTO `categorii` VALUES (1,'Telefoane/Tablete'),(2,'Electrocasnice'),(3,'Laptop/PC'),(4,'Aparate foto');
/*!40000 ALTER TABLE `categorii` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `clienti`
--

DROP TABLE IF EXISTS `clienti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `clienti` (
  `ClientID` int NOT NULL AUTO_INCREMENT,
  `Nume` varchar(45) NOT NULL,
  `Prenume` varchar(45) NOT NULL,
  `Nr_telefon` varchar(45) NOT NULL,
  `Email` varchar(45) DEFAULT NULL,
  `Oras` varchar(45) NOT NULL,
  PRIMARY KEY (`ClientID`),
  UNIQUE KEY `Nr_telefon_UNIQUE` (`Nr_telefon`)
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `clienti`
--

LOCK TABLES `clienti` WRITE;
/*!40000 ALTER TABLE `clienti` DISABLE KEYS */;
INSERT INTO `clienti` VALUES (13,'Mazilu','Gabriela','0760272480','mazilu.gabriela@yahoo.com','Constanta'),(14,'Neagu','Alexandra','0772345678','alexandrann@yahoo.com','Bucuresti'),(16,'Staicu','Marius','0760619000','marius_staicu@yahoo.com','Bucuresti'),(17,'Cezar','Anamaria','0770678902','cezar_ana@yahoo.com','Bucuresti'),(18,'Grigoras','Alexia','0760234123','grigo_alexia@yahoo.com','Bucuresti'),(19,'Marcel','Ioana','0760111668','marcel_ioana@yahoo.com','Constanta'),(20,'Popescu','Vasile','0770999555','pop_vasile@yahoo.com','Constanta'),(21,'Stanciu','Sarah','0760111660','stanciu_sarah@yahoo.com','Constanta');
/*!40000 ALTER TABLE `clienti` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamente`
--

DROP TABLE IF EXISTS `departamente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamente` (
  `DepartamentID` int NOT NULL AUTO_INCREMENT,
  `Nume_departament` varchar(45) NOT NULL,
  `Cod_departament` varchar(45) NOT NULL,
  PRIMARY KEY (`DepartamentID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamente`
--

LOCK TABLES `departamente` WRITE;
/*!40000 ALTER TABLE `departamente` DISABLE KEYS */;
INSERT INTO `departamente` VALUES (1,'Contabilitate','C022'),(2,'Service Tehnic','ST023'),(3,'Asistenta Tehnica','AT023'),(4,'Logistica','L022');
/*!40000 ALTER TABLE `departamente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dispozitive`
--

DROP TABLE IF EXISTS `dispozitive`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `dispozitive` (
  `DispozitivID` int NOT NULL AUTO_INCREMENT,
  `CategorieID` int NOT NULL,
  `ClientID` int NOT NULL,
  `Denumire` varchar(45) NOT NULL,
  `Model` varchar(45) NOT NULL,
  `Specificatii` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`DispozitivID`),
  KEY `fk_Dispozitive_Clienti_idx` (`ClientID`),
  KEY `fk_Dispozitive_Categorii` (`CategorieID`),
  CONSTRAINT `fk_Dispozitive_Categorii` FOREIGN KEY (`CategorieID`) REFERENCES `categorii` (`CategorieID`),
  CONSTRAINT `fk_Dispozitive_Clienti` FOREIGN KEY (`ClientID`) REFERENCES `clienti` (`ClientID`)
) ENGINE=InnoDB AUTO_INCREMENT=29 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dispozitive`
--

LOCK TABLES `dispozitive` WRITE;
/*!40000 ALTER TABLE `dispozitive` DISABLE KEYS */;
INSERT INTO `dispozitive` VALUES (13,1,13,'Telefon mobil','IPhone15','Black'),(14,3,16,'Laptop','Lenovo IdeaPad','Intel i7'),(15,2,13,'Aspirator vertical','Philips XC8347','21.9 kWh'),(17,1,19,'Tableta','iPad 9','Space Grey'),(18,1,18,'Telefon mobil','iPhone 15 Pro Max','Grey'),(19,4,14,'Aparat foto DSLR','Canon EOS','250D'),(21,1,19,'Telefon mobil','iPhone 14','Black'),(28,1,21,'Telefon mobil','iPhone14','Black');
/*!40000 ALTER TABLE `dispozitive` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `gestiune_servicii`
--

DROP TABLE IF EXISTS `gestiune_servicii`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `gestiune_servicii` (
  `GestiuneID` int NOT NULL AUTO_INCREMENT,
  `ServiciuID` int NOT NULL,
  `DispozitivID` int NOT NULL,
  `AngajatID` int NOT NULL,
  `Data_finalizare` date DEFAULT NULL,
  `Pret` int DEFAULT NULL,
  PRIMARY KEY (`GestiuneID`),
  KEY `fk_Servicii_has_Dispozitive_Dispozitive1_idx` (`DispozitivID`),
  KEY `fk_Servicii_has_Dispozitive_Servicii1_idx` (`ServiciuID`),
  KEY `fk_Servicii_Angajat_idx` (`AngajatID`),
  CONSTRAINT `fk_Servicii_Angajat` FOREIGN KEY (`AngajatID`) REFERENCES `angajati` (`AngajatID`),
  CONSTRAINT `fk_Servicii_has_Dispozitive_Dispozitive1` FOREIGN KEY (`DispozitivID`) REFERENCES `dispozitive` (`DispozitivID`),
  CONSTRAINT `fk_Servicii_has_Dispozitive_Servicii1` FOREIGN KEY (`ServiciuID`) REFERENCES `servicii` (`ServiciuID`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `gestiune_servicii`
--

LOCK TABLES `gestiune_servicii` WRITE;
/*!40000 ALTER TABLE `gestiune_servicii` DISABLE KEYS */;
INSERT INTO `gestiune_servicii` VALUES (1,6,13,2,'2024-01-27',80),(5,7,14,3,'2024-01-19',220),(6,3,15,2,'2024-01-19',120),(7,9,15,4,'2024-01-27',300),(8,2,14,3,'2024-02-12',500),(9,3,19,4,'2024-01-10',60),(10,6,18,3,'2024-01-21',80),(11,3,28,4,'2024-01-04',120);
/*!40000 ALTER TABLE `gestiune_servicii` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `login`
--

DROP TABLE IF EXISTS `login`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `login` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user` varchar(45) DEFAULT NULL,
  `password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `login`
--

LOCK TABLES `login` WRITE;
/*!40000 ALTER TABLE `login` DISABLE KEYS */;
INSERT INTO `login` VALUES (2,'user','parola'),(5,'MaziluGabriela','inregistrare'),(7,'PopescuMaria','parola');
/*!40000 ALTER TABLE `login` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `servicii`
--

DROP TABLE IF EXISTS `servicii`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `servicii` (
  `ServiciuID` int NOT NULL AUTO_INCREMENT,
  `Denumire` varchar(45) NOT NULL,
  `Pret` int DEFAULT NULL,
  `Piesa_necesara` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`ServiciuID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `servicii`
--

LOCK TABLES `servicii` WRITE;
/*!40000 ALTER TABLE `servicii` DISABLE KEYS */;
INSERT INTO `servicii` VALUES (1,'Inlocuire baterie',NULL,'Baterie'),(2,'Reparat placa de baza',450,NULL),(3,'Diagnosticare',130,NULL),(4,'Curatare',250,NULL),(5,'Inlocuire ecran',NULL,'Ecran '),(6,'Schimbat folie de ecran',80,'Folie de ecran'),(7,'Instalare Windows',170,'Windows'),(8,'Inlocuire componenta',250,'Curele'),(9,'Inlocuire filtru',200,'Filtru');
/*!40000 ALTER TABLE `servicii` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'mydb'
--

--
-- Dumping routines for database 'mydb'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-17 15:03:08

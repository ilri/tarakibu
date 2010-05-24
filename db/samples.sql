-- MySQL dump 10.13  Distrib 5.1.37, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: samples
-- ------------------------------------------------------
-- Server version	5.1.37-1ubuntu5.1

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
-- Temporary table structure for view `active_animals`
--

DROP TABLE IF EXISTS `active_animals`;
/*!50001 DROP VIEW IF EXISTS `active_animals`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `active_animals` (
  `id` int(11),
  `tag` varchar(11),
  `date_of_birth` datetime,
  `sex` enum('female','male'),
  `species` varchar(32),
  `owner` varchar(32),
  `location` varchar(32),
  `m_id` int(10) unsigned,
  `animal` varchar(10),
  `approximate_age` varchar(32),
  `measure_time` timestamp,
  `comment` text
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `active_samples`
--

DROP TABLE IF EXISTS `active_samples`;
/*!50001 DROP VIEW IF EXISTS `active_samples`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `active_samples` (
  `id` int(11),
  `barcode` varchar(40),
  `tag_read` int(11),
  `sample_time` timestamp,
  `latitude` double,
  `longtitude` double,
  `altitude` double,
  `hdop` float,
  `satellites` int(11),
  `comment` text,
  `raw_data` varchar(200)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `active_tags`
--

DROP TABLE IF EXISTS `active_tags`;
/*!50001 DROP VIEW IF EXISTS `active_tags`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `active_tags` (
  `rfid` varchar(15),
  `label` varchar(8),
  `color` varchar(32),
  `supplier` varchar(32),
  `type` varchar(32)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `animal_measures`
--

DROP TABLE IF EXISTS `animal_measures`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animal_measures` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `animal` varchar(10) DEFAULT NULL,
  `approximate_age` varchar(32) DEFAULT NULL,
  `measure_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `comment` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=63 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal_measures`
--

LOCK TABLES `animal_measures` WRITE;
/*!40000 ALTER TABLE `animal_measures` DISABLE KEYS */;
/*!40000 ALTER TABLE `animal_measures` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animal_replacements`
--

DROP TABLE IF EXISTS `animal_replacements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animal_replacements` (
  `new_tag` varchar(10) DEFAULT NULL,
  `replaced_tag` varchar(10) DEFAULT NULL,
  `replacement_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animal_replacements`
--

LOCK TABLES `animal_replacements` WRITE;
/*!40000 ALTER TABLE `animal_replacements` DISABLE KEYS */;
/*!40000 ALTER TABLE `animal_replacements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `animals`
--

DROP TABLE IF EXISTS `animals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `animals` (
  `tag` varchar(11) NOT NULL DEFAULT '',
  `date_of_birth` datetime DEFAULT NULL,
  `sex` enum('female','male') DEFAULT NULL,
  `species` varchar(32) DEFAULT NULL,
  `owner` varchar(32) DEFAULT NULL,
  `location` varchar(32) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `animals`
--

LOCK TABLES `animals` WRITE;
/*!40000 ALTER TABLE `animals` DISABLE KEYS */;
/*!40000 ALTER TABLE `animals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `deleted_samples`
--

DROP TABLE IF EXISTS `deleted_samples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `deleted_samples` (
  `prefix` varchar(4) NOT NULL DEFAULT '',
  `barcode` varchar(6) NOT NULL DEFAULT '',
  `delete_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`prefix`,`barcode`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `deleted_samples`
--

LOCK TABLES `deleted_samples` WRITE;
/*!40000 ALTER TABLE `deleted_samples` DISABLE KEYS */;
INSERT INTO `deleted_samples` VALUES ('BDT','002237','2010-05-11 10:22:48'),('BSR','002304','2010-05-11 10:22:48');
/*!40000 ALTER TABLE `deleted_samples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `export_animals`
--

DROP TABLE IF EXISTS `export_animals`;
/*!50001 DROP VIEW IF EXISTS `export_animals`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `export_animals` (
  `id` int(11),
  `animal_id` varchar(11),
  `organism` varchar(32),
  `age` varchar(32),
  `sex` enum('female','male'),
  `prev_tag` varchar(15),
  `location` varchar(32),
  `comments` text
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Temporary table structure for view `export_samples`
--

DROP TABLE IF EXISTS `export_samples`;
/*!50001 DROP VIEW IF EXISTS `export_samples`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `export_samples` (
  `id` int(11),
  `label` varchar(40),
  `animal_id` int(11),
  `latitude` double,
  `longtitude` double,
  `altitude` double,
  `timestamp` timestamp,
  `comments` text
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `places`
--

DROP TABLE IF EXISTS `places`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `places` (
  `name` varchar(50) NOT NULL DEFAULT '',
  `latitude` double DEFAULT NULL,
  `longtitude` double DEFAULT NULL,
  `radius` double DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `places`
--

LOCK TABLES `places` WRITE;
/*!40000 ALTER TABLE `places` DISABLE KEYS */;
INSERT INTO `places` VALUES ('ILRI',-1.269188,36.722015,1);
/*!40000 ALTER TABLE `places` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `recently_sampled`
--

DROP TABLE IF EXISTS `recently_sampled`;
/*!50001 DROP VIEW IF EXISTS `recently_sampled`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `recently_sampled` (
  `tag` varchar(11),
  `sex` enum('female','male'),
  `owner` varchar(32),
  `location` varchar(32),
  `sampled` varchar(10)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `sample_types`
--

DROP TABLE IF EXISTS `sample_types`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `sample_types` (
  `prefix` varchar(8) NOT NULL DEFAULT '',
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`prefix`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sample_types`
--

LOCK TABLES `sample_types` WRITE;
/*!40000 ALTER TABLE `sample_types` DISABLE KEYS */;
INSERT INTO `sample_types` VALUES ('MSC','Miscellaneous'),('SWB','Swab'),('BDT','EDTA Vacutainer'),('BSR','Dry Vacutainer'),('TCK','Tick'),('BHP','Heparin Vacutainer'),('BGA','<unknown>'),('BFI','<unknown>'),('L8R','Virus in Lysis Buffer'),('VTB','Virus in Transport Buffer'),('FTY','Test sample'),('AVA','avid aliquot'),('LR8','Test sample'),('IWIW17.5','iwiw sample'),('TEST','');
/*!40000 ALTER TABLE `sample_types` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary table structure for view `sampled_reads`
--

DROP TABLE IF EXISTS `sampled_reads`;
/*!50001 DROP VIEW IF EXISTS `sampled_reads`*/;
SET @saved_cs_client     = @@character_set_client;
SET character_set_client = utf8;
/*!50001 CREATE TABLE `sampled_reads` (
  `id` int(11),
  `rfid` varchar(10)
) ENGINE=MyISAM */;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `samples`
--

DROP TABLE IF EXISTS `samples`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `samples` (
  `prefix` varchar(8) NOT NULL DEFAULT '',
  `barcode` varchar(32) NOT NULL DEFAULT '',
  `tag_read` int(11) DEFAULT NULL,
  `sample_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `latitude` double DEFAULT NULL,
  `longtitude` double DEFAULT NULL,
  `altitude` double DEFAULT NULL,
  `hdop` float DEFAULT NULL,
  `satellites` int(11) DEFAULT NULL,
  `comment` text,
  `raw_data` varchar(200) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  KEY `tag` (`tag_read`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `samples`
--

LOCK TABLES `samples` WRITE;
/*!40000 ALTER TABLE `samples` DISABLE KEYS */;
/*!40000 ALTER TABLE `samples` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `species`
--

DROP TABLE IF EXISTS `species`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `species` (
  `common_name` varchar(32) NOT NULL,
  `scientific_name` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`common_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `species`
--

LOCK TABLES `species` WRITE;
/*!40000 ALTER TABLE `species` DISABLE KEYS */;
INSERT INTO `species` VALUES ('sheep','Ovis aries'),('goat','Capra aegagrus hircus'),('cattle','Bos primigenius');
/*!40000 ALTER TABLE `species` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_reads`
--

DROP TABLE IF EXISTS `tag_reads`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_reads` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rfid` varchar(10) DEFAULT NULL,
  `read_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `latitude` double DEFAULT NULL,
  `longtitude` double DEFAULT NULL,
  `altitude` double DEFAULT NULL,
  `satellites` int(11) DEFAULT NULL,
  `hdop` float DEFAULT NULL,
  `raw_data` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rfid` (`rfid`)
) ENGINE=MyISAM AUTO_INCREMENT=376 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_reads`
--

LOCK TABLES `tag_reads` WRITE;
/*!40000 ALTER TABLE `tag_reads` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_reads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tag_replacements`
--

DROP TABLE IF EXISTS `tag_replacements`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tag_replacements` (
  `rfid` varchar(15) NOT NULL,
  `label` varchar(8) DEFAULT NULL,
  `color` varchar(32) DEFAULT NULL,
  `supplier` varchar(32) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  `replaces` varchar(15) DEFAULT NULL,
  `replace_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`rfid`),
  KEY `replaces` (`replaces`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tag_replacements`
--

LOCK TABLES `tag_replacements` WRITE;
/*!40000 ALTER TABLE `tag_replacements` DISABLE KEYS */;
/*!40000 ALTER TABLE `tag_replacements` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tags`
--

DROP TABLE IF EXISTS `tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tags` (
  `rfid` varchar(15) NOT NULL,
  `label` varchar(6) DEFAULT NULL,
  `color` varchar(32) DEFAULT NULL,
  `supplier` varchar(32) DEFAULT NULL,
  `type` varchar(32) DEFAULT NULL,
  PRIMARY KEY (`rfid`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tags`
--

LOCK TABLES `tags` WRITE;
/*!40000 ALTER TABLE `tags` DISABLE KEYS */;
INSERT INTO `tags` VALUES ('900044000052788','AVD201','White','Dalton','Itag Lamb Open'),('900044000052666','AVD202','White','Dalton','Itag Lamb Open'),('900044000052842','AVD203','White','Dalton','Itag Lamb Open'),('900044000054839','AVD204','White','Dalton','Itag Lamb Open'),('900044000053135','AVD205','White','Dalton','Itag Lamb Open'),('900044000052937','AVD206','White','Dalton','Itag Lamb Open'),('900002000098600','AVD207','White','Dalton','Itag Lamb Open'),('900044000052806','AVD208','White','Dalton','Itag Lamb Open'),('900044000052689','AVD209','White','Dalton','Itag Lamb Open'),('900044000053092','AVD210','White','Dalton','Itag Lamb Open'),('900044000052881','AVD211','White','Dalton','Itag Lamb Open'),('900002000098574','AVD212','White','Dalton','Itag Lamb Open'),('900044000052572','AVD213','White','Dalton','Itag Lamb Open'),('900002000098593','AVD214','White','Dalton','Itag Lamb Open'),('900044000054765','AVD215','White','Dalton','Itag Lamb Open'),('900044000052884','AVD216','White','Dalton','Itag Lamb Open'),('900044000052665','AVD217','White','Dalton','Itag Lamb Open'),('900044000052906','AVD218','White','Dalton','Itag Lamb Open'),('900044000053031','AVD219','White','Dalton','Itag Lamb Open'),('900002000109119','AVD220','White','Dalton','Itag Lamb Open'),('900044000052928','AVD221','White','Dalton','Itag Lamb Open'),('900044000052756','AVD222','White','Dalton','Itag Lamb Open'),('900044000052913','AVD223','White','Dalton','Itag Lamb Open'),('900044000052894','AVD224','White','Dalton','Itag Lamb Open'),('900044000053021','AVD225','White','Dalton','Itag Lamb Open'),('900044000053112','AVD226','White','Dalton','Itag Lamb Open'),('900044000052669','AVD227','White','Dalton','Itag Lamb Open'),('900044000052715','AVD228','White','Dalton','Itag Lamb Open'),('900044000053060','AVD229','White','Dalton','Itag Lamb Open'),('900044000052711','AVD230','White','Dalton','Itag Lamb Open'),('900044000052735','AVD231','White','Dalton','Itag Lamb Open'),('900044000052905','AVD232','White','Dalton','Itag Lamb Open'),('900044000052671','AVD233','White','Dalton','Itag Lamb Open'),('900044000052929','AVD234','White','Dalton','Itag Lamb Open'),('900044000052681','AVD235','White','Dalton','Itag Lamb Open'),('900044000052746','AVD236','White','Dalton','Itag Lamb Open'),('900044000052663','AVD237','White','Dalton','Itag Lamb Open'),('900044000052855','AVD238','White','Dalton','Itag Lamb Open'),('900002000098565','AVD239','White','Dalton','Itag Lamb Open'),('900044000052729','AVD240','White','Dalton','Itag Lamb Open'),('900044000052687','AVD241','White','Dalton','Itag Lamb Open'),('900044000052722','AVD242','White','Dalton','Itag Lamb Open'),('900044000053064','AVD243','White','Dalton','Itag Lamb Open'),('900044000052624','AVD244','White','Dalton','Itag Lamb Open'),('900044000052683','AVD245','White','Dalton','Itag Lamb Open'),('900044000052736','AVD246','White','Dalton','Itag Lamb Open'),('900044000052652','AVD247','White','Dalton','Itag Lamb Open'),('900044000052703','AVD248','White','Dalton','Itag Lamb Open'),('900044000052667','AVD249','White','Dalton','Itag Lamb Open'),('900044000052654','AVD250','White','Dalton','Itag Lamb Open'),('900044000053109','AVD251','White','Dalton','Itag Lamb Open'),('900044000052733','AVD252','White','Dalton','Itag Lamb Open'),('900044000053037','AVD253','White','Dalton','Itag Lamb Open'),('900044000052890','AVD254','White','Dalton','Itag Lamb Open'),('900044000052651','AVD255','White','Dalton','Itag Lamb Open'),('900044000052743','AVD256','White','Dalton','Itag Lamb Open'),('900044000052559','AVD257','White','Dalton','Itag Lamb Open'),('900044000053105','AVD258','White','Dalton','Itag Lamb Open'),('900044000053144','AVD259','White','Dalton','Itag Lamb Open'),('900044000052943','AVD260','White','Dalton','Itag Lamb Open'),('900044000052748','AVD261','White','Dalton','Itag Lamb Open'),('900044000052554','AVD262','White','Dalton','Itag Lamb Open'),('900044000052690','AVD263','White','Dalton','Itag Lamb Open'),('900044000052555','AVD264','White','Dalton','Itag Lamb Open'),('900044000052935','AVD265','White','Dalton','Itag Lamb Open'),('900044000052923','AVD266','White','Dalton','Itag Lamb Open'),('900044000052707','AVD267','White','Dalton','Itag Lamb Open'),('900044000052718','AVD268','White','Dalton','Itag Lamb Open'),('900044000052709','AVD269','White','Dalton','Itag Lamb Open'),('900044000052710','AVD270','White','Dalton','Itag Lamb Open'),('900044000052629','AVD271','White','Dalton','Itag Lamb Open'),('900044000052661','AVD272','White','Dalton','Itag Lamb Open'),('900044000052631','AVD273','White','Dalton','Itag Lamb Open'),('900044000052700','AVD274','White','Dalton','Itag Lamb Open'),('900044000052721','AVD275','White','Dalton','Itag Lamb Open'),('900044000052741','AVD276','White','Dalton','Itag Lamb Open'),('900044000052705','AVD277','White','Dalton','Itag Lamb Open'),('900044000052698','AVD278','White','Dalton','Itag Lamb Open'),('900044000052731','AVD279','White','Dalton','Itag Lamb Open'),('900044000052695','AVD280','White','Dalton','Itag Lamb Open'),('900044000052734','AVD281','White','Dalton','Itag Lamb Open'),('900044000052723','AVD282','White','Dalton','Itag Lamb Open'),('900044000052600','AVD283','White','Dalton','Itag Lamb Open'),('900044000052673','AVD284','White','Dalton','Itag Lamb Open'),('900044000052738','AVD285','White','Dalton','Itag Lamb Open'),('900044000052630','AVD286','White','Dalton','Itag Lamb Open'),('900044000052720','AVD287','White','Dalton','Itag Lamb Open'),('900044000052604','AVD288','White','Dalton','Itag Lamb Open'),('900044000052725','AVD289','White','Dalton','Itag Lamb Open'),('900044000052659','AVD290','White','Dalton','Itag Lamb Open'),('900044000052650','AVD291','White','Dalton','Itag Lamb Open'),('900044000052708','AVD292','White','Dalton','Itag Lamb Open'),('900044000052616','AVD293','White','Dalton','Itag Lamb Open'),('900044000052730','AVD294','White','Dalton','Itag Lamb Open'),('900044000052706','AVD295','White','Dalton','Itag Lamb Open'),('900044000052612','AVD296','White','Dalton','Itag Lamb Open'),('900044000052702','AVD297','White','Dalton','Itag Lamb Open'),('900044000052713','AVD298','White','Dalton','Itag Lamb Open'),('900044000052632','AVD299','White','Dalton','Itag Lamb Open'),('900044000052644','AVD300','White','Dalton','Itag Lamb Open'),('900044000052727','AVD301','White','Dalton','Itag Lamb Open'),('900044000052639','AVD302','White','Dalton','Itag Lamb Open'),('900044000052551','AVD303','White','Dalton','Itag Lamb Open'),('900044000052607','AVD304','White','Dalton','Itag Lamb Open'),('900044000052714','AVD305','White','Dalton','Itag Lamb Open'),('900044000052574','AVD306','White','Dalton','Itag Lamb Open'),('900044000052668','AVD307','White','Dalton','Itag Lamb Open'),('900044000052556','AVD308','White','Dalton','Itag Lamb Open'),('900044000052648','AVD309','White','Dalton','Itag Lamb Open'),('900044000052623','AVD310','White','Dalton','Itag Lamb Open'),('900044000052587','AVD311','White','Dalton','Itag Lamb Open'),('900044000052580','AVD312','White','Dalton','Itag Lamb Open'),('900044000052588','AVD313','White','Dalton','Itag Lamb Open'),('900044000052692','AVD314','White','Dalton','Itag Lamb Open'),('900044000052628','AVD315','White','Dalton','Itag Lamb Open'),('900044000052638','AVD316','White','Dalton','Itag Lamb Open'),('900044000052608','AVD317','White','Dalton','Itag Lamb Open'),('900044000052575','AVD318','White','Dalton','Itag Lamb Open'),('900044000052613','AVD319','White','Dalton','Itag Lamb Open'),('900044000052717','AVD320','White','Dalton','Itag Lamb Open'),('900044000052739','AVD321','White','Dalton','Itag Lamb Open'),('900044000052606','AVD322','White','Dalton','Itag Lamb Open'),('900044000052640','AVD323','White','Dalton','Itag Lamb Open'),('900044000052594','AVD324','White','Dalton','Itag Lamb Open'),('900044000052570','AVD325','White','Dalton','Itag Lamb Open'),('900044000052591','AVD326','White','Dalton','Itag Lamb Open'),('900044000052620','AVD327','White','Dalton','Itag Lamb Open'),('900044000052579','AVD328','White','Dalton','Itag Lamb Open'),('900044000052712','AVD329','White','Dalton','Itag Lamb Open'),('900044000052568','AVD330','White','Dalton','Itag Lamb Open'),('900044000052550','AVD331','White','Dalton','Itag Lamb Open'),('900044000052567','AVD332','White','Dalton','Itag Lamb Open'),('900044000052619','AVD333','White','Dalton','Itag Lamb Open'),('900044000052627','AVD334','White','Dalton','Itag Lamb Open'),('900044000052643','AVD335','White','Dalton','Itag Lamb Open'),('900044000052603','AVD336','White','Dalton','Itag Lamb Open'),('900044000052626','AVD337','White','Dalton','Itag Lamb Open'),('900044000052601','AVD338','White','Dalton','Itag Lamb Open'),('900044000052602','AVD339','White','Dalton','Itag Lamb Open'),('900044000052621','AVD340','White','Dalton','Itag Lamb Open'),('900044000052577','AVD341','White','Dalton','Itag Lamb Open'),('900044000052576','AVD342','White','Dalton','Itag Lamb Open'),('900044000052562','AVD343','White','Dalton','Itag Lamb Open'),('900044000052633','AVD344','White','Dalton','Itag Lamb Open'),('900044000052617','AVD345','White','Dalton','Itag Lamb Open'),('900044000052618','AVD346','White','Dalton','Itag Lamb Open'),('900044000052636','AVD347','White','Dalton','Itag Lamb Open'),('900044000052622','AVD348','White','Dalton','Itag Lamb Open'),('900044000052615','AVD349','White','Dalton','Itag Lamb Open'),('900044000052595','AVD350','White','Dalton','Itag Lamb Open'),('900044000052598','AVD351','White','Dalton','Itag Lamb Open'),('900044000052563','AVD352','White','Dalton','Itag Lamb Open'),('900044000052593','AVD353','White','Dalton','Itag Lamb Open'),('900044000052609','AVD354','White','Dalton','Itag Lamb Open'),('900044000052569','AVD355','White','Dalton','Itag Lamb Open'),('900044000052571','AVD356','White','Dalton','Itag Lamb Open'),('900044000052584','AVD357','White','Dalton','Itag Lamb Open'),('900044000052614','AVD358','White','Dalton','Itag Lamb Open'),('900044000052641','AVD359','White','Dalton','Itag Lamb Open'),('900044000052583','AVD360','White','Dalton','Itag Lamb Open'),('900044000052647','AVD361','White','Dalton','Itag Lamb Open'),('900044000052642','AVD362','White','Dalton','Itag Lamb Open'),('900044000052646','AVD363','White','Dalton','Itag Lamb Open'),('900044000052557','AVD364','White','Dalton','Itag Lamb Open'),('900044000052589','AVD365','White','Dalton','Itag Lamb Open'),('900044000052549','AVD366','White','Dalton','Itag Lamb Open'),('900044000052599','AVD367','White','Dalton','Itag Lamb Open'),('900044000052581','AVD368','White','Dalton','Itag Lamb Open'),('900044000052605','AVD369','White','Dalton','Itag Lamb Open'),('900044000052634','AVD370','White','Dalton','Itag Lamb Open'),('900044000052586','AVD371','White','Dalton','Itag Lamb Open'),('900044000052573','AVD372','White','Dalton','Itag Lamb Open'),('900044000052597','AVD373','White','Dalton','Itag Lamb Open'),('900044000052610','AVD374','White','Dalton','Itag Lamb Open'),('900044000052561','AVD375','White','Dalton','Itag Lamb Open'),('900044000052585','AVD376','White','Dalton','Itag Lamb Open'),('900044000052582','AVD377','White','Dalton','Itag Lamb Open'),('900044000052590','AVD378','White','Dalton','Itag Lamb Open'),('900044000052564','AVD379','White','Dalton','Itag Lamb Open'),('900044000052635','AVD380','White','Dalton','Itag Lamb Open'),('900044000052611','AVD381','White','Dalton','Itag Lamb Open'),('900044000052552','AVD382','White','Dalton','Itag Lamb Open'),('900044000052592','AVD383','White','Dalton','Itag Lamb Open'),('900044000052560','AVD384','White','Dalton','Itag Lamb Open'),('900044000052637','AVD385','White','Dalton','Itag Lamb Open'),('900044000052625','AVD386','White','Dalton','Itag Lamb Open'),('900044000052596','AVD387','White','Dalton','Itag Lamb Open'),('900044000052558','AVD388','White','Dalton','Itag Lamb Open'),('900044000052645','AVD389','White','Dalton','Itag Lamb Open'),('900044000052565','AVD390','White','Dalton','Itag Lamb Open'),('900044000052553','AVD391','White','Dalton','Itag Lamb Open'),('900044000052578','AVD392','White','Dalton','Itag Lamb Open'),('900044000052566','AVD393','White','Dalton','Itag Lamb Open'),('900044000052664','AVD394','White','Dalton','Itag Lamb Open'),('900044000052744','AVD395','White','Dalton','Itag Lamb Open'),('900044000052649','AVD396','White','Dalton','Itag Lamb Open'),('900044000052694','AVD397','White','Dalton','Itag Lamb Open'),('900044000052672','AVD398','White','Dalton','Itag Lamb Open'),('900044000052737','AVD399','White','Dalton','Itag Lamb Open'),('900044000052662','AVD400','White','Dalton','Itag Lamb Open'),('900044000052697','AVD401','White','Dalton','Itag Lamb Open'),('900044000052704','AVD402','White','Dalton','Itag Lamb Open'),('900044000052677','AVD403','White','Dalton','Itag Lamb Open'),('900044000052745','AVD404','White','Dalton','Itag Lamb Open'),('900044000052726','AVD405','White','Dalton','Itag Lamb Open'),('900044000052742','AVD406','White','Dalton','Itag Lamb Open'),('900044000052724','AVD407','White','Dalton','Itag Lamb Open'),('900044000052688','AVD408','White','Dalton','Itag Lamb Open'),('900044000052699','AVD409','White','Dalton','Itag Lamb Open'),('900044000052686','AVD410','White','Dalton','Itag Lamb Open'),('900044000052696','AVD411','White','Dalton','Itag Lamb Open'),('900044000052728','AVD412','White','Dalton','Itag Lamb Open'),('900044000052716','AVD413','White','Dalton','Itag Lamb Open'),('900044000052747','AVD414','White','Dalton','Itag Lamb Open'),('900044000052658','AVD415','White','Dalton','Itag Lamb Open'),('900044000052701','AVD416','White','Dalton','Itag Lamb Open'),('900044000052678','AVD417','White','Dalton','Itag Lamb Open'),('900044000052653','AVD418','White','Dalton','Itag Lamb Open'),('900044000052657','AVD419','White','Dalton','Itag Lamb Open'),('900044000052719','AVD420','White','Dalton','Itag Lamb Open'),('900044000052679','AVD421','White','Dalton','Itag Lamb Open'),('900044000052674','AVD422','White','Dalton','Itag Lamb Open'),('900044000052670','AVD423','White','Dalton','Itag Lamb Open'),('900044000052660','AVD424','White','Dalton','Itag Lamb Open'),('900044000052685','AVD425','White','Dalton','Itag Lamb Open'),('900044000052691','AVD426','White','Dalton','Itag Lamb Open'),('900044000052732','AVD427','White','Dalton','Itag Lamb Open'),('900044000052684','AVD428','White','Dalton','Itag Lamb Open'),('900044000052655','AVD429','White','Dalton','Itag Lamb Open'),('900044000052680','AVD430','White','Dalton','Itag Lamb Open'),('900044000052682','AVD431','White','Dalton','Itag Lamb Open'),('900044000052675','AVD432','White','Dalton','Itag Lamb Open'),('900044000052676','AVD433','White','Dalton','Itag Lamb Open'),('900044000052693','AVD434','White','Dalton','Itag Lamb Open'),('900044000052740','AVD435','White','Dalton','Itag Lamb Open'),('900044000052656','AVD436','White','Dalton','Itag Lamb Open'),('900044000053079','AVD437','White','Dalton','Itag Lamb Open'),('900044000052889','AVD438','White','Dalton','Itag Lamb Open'),('900002000109163','AVD439','White','Dalton','Itag Lamb Open'),('900044000052955','AVD440','White','Dalton','Itag Lamb Open'),('900002000109191','AVD441','White','Dalton','Itag Lamb Open'),('900044000053132','AVD442','White','Dalton','Itag Lamb Open'),('900044000052892','AVD443','White','Dalton','Itag Lamb Open'),('900044000053114','AVD444','White','Dalton','Itag Lamb Open'),('900044000053084','AVD445','White','Dalton','Itag Lamb Open'),('900044000052770','AVD446','White','Dalton','Itag Lamb Open'),('900044000053035','AVD447','White','Dalton','Itag Lamb Open'),('900044000052857','AVD448','White','Dalton','Itag Lamb Open'),('900044000052856','AVD449','White','Dalton','Itag Lamb Open'),('900044000053125','AVD450','White','Dalton','Itag Lamb Open'),('900002000109187','AVD451','White','Dalton','Itag Lamb Open'),('900044000053081','AVD452','White','Dalton','Itag Lamb Open'),('900002000109164','AVD453','White','Dalton','Itag Lamb Open'),('900044000053062','AVD454','White','Dalton','Itag Lamb Open'),('900002000109194','AVD455','White','Dalton','Itag Lamb Open'),('900044000053052','AVD456','White','Dalton','Itag Lamb Open'),('900044000053128','AVD457','White','Dalton','Itag Lamb Open'),('900044000053089','AVD458','White','Dalton','Itag Lamb Open'),('900002000109101','AVD459','White','Dalton','Itag Lamb Open'),('900044000053005','AVD460','White','Dalton','Itag Lamb Open'),('900044000053055','AVD461','White','Dalton','Itag Lamb Open'),('900044000053137','AVD462','White','Dalton','Itag Lamb Open'),('900044000053094','AVD463','White','Dalton','Itag Lamb Open'),('900044000052958','AVD464','White','Dalton','Itag Lamb Open'),('900044000052885','AVD465','White','Dalton','Itag Lamb Open'),('900044000053102','AVD466','White','Dalton','Itag Lamb Open'),('900044000053073','AVD467','White','Dalton','Itag Lamb Open'),('900044000052902','AVD468','White','Dalton','Itag Lamb Open'),('900044000053110','AVD469','White','Dalton','Itag Lamb Open'),('900044000052804','AVD470','White','Dalton','Itag Lamb Open'),('900002000109125','AVD471','White','Dalton','Itag Lamb Open'),('900044000052957','AVD472','White','Dalton','Itag Lamb Open'),('900002000109141','AVD473','White','Dalton','Itag Lamb Open'),('900044000053088','AVD474','White','Dalton','Itag Lamb Open'),('900044000053056','AVD475','White','Dalton','Itag Lamb Open'),('900044000053002','AVD476','White','Dalton','Itag Lamb Open'),('900044000052970','AVD477','White','Dalton','Itag Lamb Open'),('900044000053018','AVD478','White','Dalton','Itag Lamb Open'),('900044000053030','AVD479','White','Dalton','Itag Lamb Open'),('900044000052965','AVD480','White','Dalton','Itag Lamb Open'),('900044000053048','AVD481','White','Dalton','Itag Lamb Open'),('900044000053083','AVD482','White','Dalton','Itag Lamb Open'),('900044000052960','AVD483','White','Dalton','Itag Lamb Open'),('900044000052971','AVD484','White','Dalton','Itag Lamb Open'),('900044000052974','AVD485','White','Dalton','Itag Lamb Open'),('900044000053015','AVD486','White','Dalton','Itag Lamb Open'),('900044000053101','AVD487','White','Dalton','Itag Lamb Open'),('900044000053145','AVD488','White','Dalton','Itag Lamb Open'),('900002000109143','AVD489','White','Dalton','Itag Lamb Open'),('900044000053124','AVD490','White','Dalton','Itag Lamb Open'),('900044000053017','AVD491','White','Dalton','Itag Lamb Open'),('900002000109042','AVD492','White','Dalton','Itag Lamb Open'),('900002000109154','AVD493','White','Dalton','Itag Lamb Open'),('900044000053098','AVD494','White','Dalton','Itag Lamb Open'),('900044000053077','AVD495','White','Dalton','Itag Lamb Open'),('900044000053028','AVD496','White','Dalton','Itag Lamb Open'),('900044000052975','AVD497','White','Dalton','Itag Lamb Open'),('900044000053139','AVD498','White','Dalton','Itag Lamb Open'),('900044000053140','AVD499','White','Dalton','Itag Lamb Open'),('900044000053009','AVD500','White','Dalton','Itag Lamb Open'),('900044000053106','AVD501','White','Dalton','Itag Lamb Open'),('900044000053042','AVD502','White','Dalton','Itag Lamb Open'),('900044000052961','AVD503','White','Dalton','Itag Lamb Open'),('900044000053011','AVD504','White','Dalton','Itag Lamb Open'),('900044000053029','AVD505','White','Dalton','Itag Lamb Open'),('900044000053006','AVD506','White','Dalton','Itag Lamb Open'),('900044000053070','AVD507','White','Dalton','Itag Lamb Open'),('900044000053040','AVD508','White','Dalton','Itag Lamb Open'),('900044000052993','AVD509','White','Dalton','Itag Lamb Open'),('900044000053007','AVD510','White','Dalton','Itag Lamb Open'),('900044000053020','AVD511','White','Dalton','Itag Lamb Open'),('900044000052962','AVD512','White','Dalton','Itag Lamb Open'),('900044000052987','AVD513','White','Dalton','Itag Lamb Open'),('900044000052956','AVD514','White','Dalton','Itag Lamb Open'),('900044000053108','AVD515','White','Dalton','Itag Lamb Open'),('900044000052969','AVD516','White','Dalton','Itag Lamb Open'),('900044000052952','AVD517','White','Dalton','Itag Lamb Open'),('900044000052998','AVD518','White','Dalton','Itag Lamb Open'),('900044000052979','AVD519','White','Dalton','Itag Lamb Open'),('900044000053019','AVD520','White','Dalton','Itag Lamb Open'),('900044000052822','AVD521','White','Dalton','Itag Lamb Open'),('900044000053023','AVD522','White','Dalton','Itag Lamb Open'),('900044000052990','AVD523','White','Dalton','Itag Lamb Open'),('900044000052983','AVD524','White','Dalton','Itag Lamb Open'),('900044000053087','AVD525','White','Dalton','Itag Lamb Open'),('900044000053004','AVD526','White','Dalton','Itag Lamb Open'),('900044000052968','AVD527','White','Dalton','Itag Lamb Open'),('900044000053001','AVD528','White','Dalton','Itag Lamb Open'),('900044000052966','AVD529','White','Dalton','Itag Lamb Open'),('900044000053016','AVD530','White','Dalton','Itag Lamb Open'),('900044000053047','AVD531','White','Dalton','Itag Lamb Open'),('900044000053130','AVD532','White','Dalton','Itag Lamb Open'),('900044000052977','AVD533','White','Dalton','Itag Lamb Open'),('900044000052981','AVD534','White','Dalton','Itag Lamb Open'),('900044000053027','AVD535','White','Dalton','Itag Lamb Open'),('900044000052996','AVD536','White','Dalton','Itag Lamb Open'),('900044000052982','AVD537','White','Dalton','Itag Lamb Open'),('900044000053003','AVD538','White','Dalton','Itag Lamb Open'),('900044000053038','AVD539','White','Dalton','Itag Lamb Open'),('900044000052980','AVD540','White','Dalton','Itag Lamb Open'),('900044000052959','AVD541','White','Dalton','Itag Lamb Open'),('900044000053014','AVD542','White','Dalton','Itag Lamb Open'),('900044000053065','AVD543','White','Dalton','Itag Lamb Open'),('900044000053036','AVD544','White','Dalton','Itag Lamb Open'),('900044000052976','AVD545','White','Dalton','Itag Lamb Open'),('900044000053010','AVD546','White','Dalton','Itag Lamb Open'),('900044000052986','AVD547','White','Dalton','Itag Lamb Open'),('900044000053025','AVD548','White','Dalton','Itag Lamb Open'),('900044000053033','AVD549','White','Dalton','Itag Lamb Open'),('900044000052973','AVD550','White','Dalton','Itag Lamb Open'),('900044000053032','AVD551','White','Dalton','Itag Lamb Open'),('900044000053008','AVD552','White','Dalton','Itag Lamb Open'),('900044000052992','AVD553','White','Dalton','Itag Lamb Open'),('900044000052997','AVD554','White','Dalton','Itag Lamb Open'),('900044000053012','AVD555','White','Dalton','Itag Lamb Open'),('900044000053024','AVD556','White','Dalton','Itag Lamb Open'),('900044000052972','AVD557','White','Dalton','Itag Lamb Open'),('900044000052991','AVD558','White','Dalton','Itag Lamb Open'),('900044000052954','AVD559','White','Dalton','Itag Lamb Open'),('900044000053013','AVD560','White','Dalton','Itag Lamb Open'),('900044000053046','AVD561','White','Dalton','Itag Lamb Open'),('900044000053041','AVD562','White','Dalton','Itag Lamb Open'),('900044000052963','AVD563','White','Dalton','Itag Lamb Open'),('900044000053026','AVD564','White','Dalton','Itag Lamb Open'),('900044000052994','AVD565','White','Dalton','Itag Lamb Open'),('900044000052985','AVD566','White','Dalton','Itag Lamb Open'),('900044000053045','AVD567','White','Dalton','Itag Lamb Open'),('900044000052999','AVD568','White','Dalton','Itag Lamb Open'),('900044000053022','AVD569','White','Dalton','Itag Lamb Open'),('900044000052984','AVD570','White','Dalton','Itag Lamb Open'),('900044000053034','AVD571','White','Dalton','Itag Lamb Open'),('900044000052995','AVD572','White','Dalton','Itag Lamb Open'),('900044000052953','AVD573','White','Dalton','Itag Lamb Open'),('900044000052964','AVD574','White','Dalton','Itag Lamb Open'),('900044000053000','AVD575','White','Dalton','Itag Lamb Open'),('900044000053043','AVD576','White','Dalton','Itag Lamb Open'),('900044000052989','AVD577','White','Dalton','Itag Lamb Open'),('900044000052978','AVD578','White','Dalton','Itag Lamb Open'),('900044000052950','AVD579','White','Dalton','Itag Lamb Open'),('900044000053044','AVD580','White','Dalton','Itag Lamb Open'),('900044000052949','AVD581','White','Dalton','Itag Lamb Open'),('900044000052951','AVD582','White','Dalton','Itag Lamb Open'),('900044000052988','AVD583','White','Dalton','Itag Lamb Open'),('900044000053039','AVD584','White','Dalton','Itag Lamb Open'),('900044000052967','AVD585','White','Dalton','Itag Lamb Open'),('900044000053063','AVD586','White','Dalton','Itag Lamb Open'),('900044000053053','AVD587','White','Dalton','Itag Lamb Open'),('900044000053142','AVD588','White','Dalton','Itag Lamb Open'),('900044000053080','AVD589','White','Dalton','Itag Lamb Open'),('900002000109161','AVD590','White','Dalton','Itag Lamb Open'),('900044000053133','AVD591','White','Dalton','Itag Lamb Open'),('900044000053100','AVD592','White','Dalton','Itag Lamb Open'),('900044000053103','AVD593','White','Dalton','Itag Lamb Open'),('900044000053148','AVD594','White','Dalton','Itag Lamb Open'),('900044000053113','AVD595','White','Dalton','Itag Lamb Open'),('900044000053121','AVD596','White','Dalton','Itag Lamb Open'),('900044000053095','AVD597','White','Dalton','Itag Lamb Open'),('900044000053119','AVD598','White','Dalton','Itag Lamb Open'),('900044000053123','AVD599','White','Dalton','Itag Lamb Open'),('900044000053117','AVD600','White','Dalton','Itag Lamb Open'),('900044000053076','AVD601','White','Dalton','Itag Lamb Open'),('900044000053107','AVD602','White','Dalton','Itag Lamb Open'),('900044000053116','AVD603','White','Dalton','Itag Lamb Open'),('900044000053099','AVD604','White','Dalton','Itag Lamb Open'),('900044000053147','AVD605','White','Dalton','Itag Lamb Open'),('900044000053111','AVD606','White','Dalton','Itag Lamb Open'),('900044000053085','AVD607','White','Dalton','Itag Lamb Open'),('900044000053059','AVD608','White','Dalton','Itag Lamb Open'),('900044000053097','AVD609','White','Dalton','Itag Lamb Open'),('900044000053120','AVD610','White','Dalton','Itag Lamb Open'),('900044000053138','AVD611','White','Dalton','Itag Lamb Open'),('900044000053093','AVD612','White','Dalton','Itag Lamb Open'),('900044000053078','AVD613','White','Dalton','Itag Lamb Open'),('900044000053069','AVD614','White','Dalton','Itag Lamb Open'),('900044000053146','AVD615','White','Dalton','Itag Lamb Open'),('900044000053066','AVD616','White','Dalton','Itag Lamb Open'),('900044000053104','AVD617','White','Dalton','Itag Lamb Open'),('900044000053049','AVD618','White','Dalton','Itag Lamb Open'),('900044000053086','AVD619','White','Dalton','Itag Lamb Open'),('900044000053118','AVD620','White','Dalton','Itag Lamb Open'),('900044000053051','AVD621','White','Dalton','Itag Lamb Open'),('900044000053134','AVD622','White','Dalton','Itag Lamb Open'),('900044000053067','AVD623','White','Dalton','Itag Lamb Open'),('900044000053050','AVD624','White','Dalton','Itag Lamb Open'),('900044000053090','AVD625','White','Dalton','Itag Lamb Open'),('900044000053136','AVD626','White','Dalton','Itag Lamb Open'),('900044000053068','AVD627','White','Dalton','Itag Lamb Open'),('900044000053074','AVD628','White','Dalton','Itag Lamb Open'),('900044000053057','AVD629','White','Dalton','Itag Lamb Open'),('900044000053072','AVD630','White','Dalton','Itag Lamb Open'),('900044000053082','AVD631','White','Dalton','Itag Lamb Open'),('900044000053126','AVD632','White','Dalton','Itag Lamb Open'),('900044000053127','AVD633','White','Dalton','Itag Lamb Open'),('900044000053141','AVD634','White','Dalton','Itag Lamb Open'),('900044000053058','AVD635','White','Dalton','Itag Lamb Open'),('900044000053143','AVD636','White','Dalton','Itag Lamb Open'),('900044000053071','AVD637','White','Dalton','Itag Lamb Open'),('900044000053129','AVD638','White','Dalton','Itag Lamb Open'),('900044000053096','AVD639','White','Dalton','Itag Lamb Open'),('900044000053115','AVD640','White','Dalton','Itag Lamb Open'),('900044000053075','AVD641','White','Dalton','Itag Lamb Open'),('900044000053122','AVD642','White','Dalton','Itag Lamb Open'),('900044000053054','AVD643','White','Dalton','Itag Lamb Open'),('900044000053091','AVD644','White','Dalton','Itag Lamb Open'),('900044000052939','AVD645','White','Dalton','Itag Lamb Open'),('900044000052852','AVD646','White','Dalton','Itag Lamb Open'),('900044000052930','AVD647','White','Dalton','Itag Lamb Open'),('900002000109155','AVD648','White','Dalton','Itag Lamb Open'),('900044000052886','AVD649','White','Dalton','Itag Lamb Open'),('900002000109151','AVD650','White','Dalton','Itag Lamb Open'),('900002000109133','AVD651','White','Dalton','Itag Lamb Open'),('900044000052921','AVD652','White','Dalton','Itag Lamb Open'),('900002000109167','AVD653','White','Dalton','Itag Lamb Open'),('900002000109128','AVD654','White','Dalton','Itag Lamb Open'),('900044000052850','AVD655','White','Dalton','Itag Lamb Open'),('900044000052910','AVD656','White','Dalton','Itag Lamb Open'),('900044000052911','AVD657','White','Dalton','Itag Lamb Open'),('900044000052836','AVD658','White','Dalton','Itag Lamb Open'),('900044000052872','AVD659','White','Dalton','Itag Lamb Open'),('900002000109059','AVD660','White','Dalton','Itag Lamb Open'),('900002000109118','AVD661','White','Dalton','Itag Lamb Open'),('900002000109171','AVD662','White','Dalton','Itag Lamb Open'),('900002000109127','AVD663','White','Dalton','Itag Lamb Open'),('900002000109172','AVD664','White','Dalton','Itag Lamb Open'),('900002000109195','AVD665','White','Dalton','Itag Lamb Open'),('900044000052867','AVD666','White','Dalton','Itag Lamb Open'),('900002000109190','AVD667','White','Dalton','Itag Lamb Open'),('900002000109165','AVD668','White','Dalton','Itag Lamb Open'),('900002000109166','AVD669','White','Dalton','Itag Lamb Open'),('900002000109122','AVD670','White','Dalton','Itag Lamb Open'),('900002000109159','AVD671','White','Dalton','Itag Lamb Open'),('900002000109179','AVD672','White','Dalton','Itag Lamb Open'),('900002000109115','AVD673','White','Dalton','Itag Lamb Open'),('900002000109109','AVD674','White','Dalton','Itag Lamb Open'),('900002000109197','AVD675','White','Dalton','Itag Lamb Open'),('900002000109153','AVD676','White','Dalton','Itag Lamb Open'),('900002000109158','AVD677','White','Dalton','Itag Lamb Open'),('900002000109120','AVD678','White','Dalton','Itag Lamb Open'),('900002000109193','AVD679','White','Dalton','Itag Lamb Open'),('900002000109169','AVD680','White','Dalton','Itag Lamb Open'),('900002000109168','AVD681','White','Dalton','Itag Lamb Open'),('900002000109173','AVD682','White','Dalton','Itag Lamb Open'),('900002000109162','AVD683','White','Dalton','Itag Lamb Open'),('900044000052945','AVD684','White','Dalton','Itag Lamb Open'),('900002000109160','AVD685','White','Dalton','Itag Lamb Open'),('900002000109177','AVD686','White','Dalton','Itag Lamb Open'),('900002000109198','AVD687','White','Dalton','Itag Lamb Open'),('900002000109147','AVD688','White','Dalton','Itag Lamb Open'),('900002000109189','AVD689','White','Dalton','Itag Lamb Open'),('900002000109156','AVD690','White','Dalton','Itag Lamb Open'),('900002000109184','AVD691','White','Dalton','Itag Lamb Open'),('900002000109186','AVD692','White','Dalton','Itag Lamb Open'),('900002000109180','AVD693','White','Dalton','Itag Lamb Open'),('900002000109102','AVD694','White','Dalton','Itag Lamb Open'),('900002000109110','AVD695','White','Dalton','Itag Lamb Open'),('900002000109157','AVD696','White','Dalton','Itag Lamb Open'),('900002000109185','AVD697','White','Dalton','Itag Lamb Open'),('900002000109149','AVD698','White','Dalton','Itag Lamb Open'),('900002000109136','AVD699','White','Dalton','Itag Lamb Open'),('900002000109146','AVD700','White','Dalton','Itag Lamb Open'),('900002000109112','AVD701','White','Dalton','Itag Lamb Open'),('900002000109200','AVD702','White','Dalton','Itag Lamb Open'),('900002000109139','AVD703','White','Dalton','Itag Lamb Open'),('900002000109192','AVD704','White','Dalton','Itag Lamb Open'),('900002000109188','AVD705','White','Dalton','Itag Lamb Open'),('900002000109176','AVD706','White','Dalton','Itag Lamb Open'),('900002000109142','AVD707','White','Dalton','Itag Lamb Open'),('900002000109170','AVD708','White','Dalton','Itag Lamb Open'),('900002000109124','AVD709','White','Dalton','Itag Lamb Open'),('900002000109132','AVD710','White','Dalton','Itag Lamb Open'),('900002000109108','AVD711','White','Dalton','Itag Lamb Open'),('900002000109182','AVD712','White','Dalton','Itag Lamb Open'),('900002000109183','AVD713','White','Dalton','Itag Lamb Open'),('900002000109140','AVD714','White','Dalton','Itag Lamb Open'),('900002000109181','AVD715','White','Dalton','Itag Lamb Open'),('900002000109126','AVD716','White','Dalton','Itag Lamb Open'),('900002000109174','AVD717','White','Dalton','Itag Lamb Open'),('900002000109106','AVD718','White','Dalton','Itag Lamb Open'),('900002000109114','AVD719','White','Dalton','Itag Lamb Open'),('900002000109113','AVD720','White','Dalton','Itag Lamb Open'),('900002000109196','AVD721','White','Dalton','Itag Lamb Open'),('900002000109107','AVD722','White','Dalton','Itag Lamb Open'),('900002000109116','AVD723','White','Dalton','Itag Lamb Open'),('900002000109123','AVD724','White','Dalton','Itag Lamb Open'),('900002000109105','AVD725','White','Dalton','Itag Lamb Open'),('900002000109131','AVD726','White','Dalton','Itag Lamb Open'),('900002000109129','AVD727','White','Dalton','Itag Lamb Open'),('900002000109130','AVD728','White','Dalton','Itag Lamb Open'),('900002000109134','AVD729','White','Dalton','Itag Lamb Open'),('900002000109178','AVD730','White','Dalton','Itag Lamb Open'),('900002000109104','AVD731','White','Dalton','Itag Lamb Open'),('900002000109199','AVD732','White','Dalton','Itag Lamb Open'),('900002000109121','AVD733','White','Dalton','Itag Lamb Open'),('900002000109103','AVD734','White','Dalton','Itag Lamb Open'),('900002000109111','AVD735','White','Dalton','Itag Lamb Open'),('900002000109144','AVD736','White','Dalton','Itag Lamb Open'),('900002000109117','AVD737','White','Dalton','Itag Lamb Open'),('900002000109148','AVD738','White','Dalton','Itag Lamb Open'),('900002000109138','AVD739','White','Dalton','Itag Lamb Open'),('900002000109145','AVD740','White','Dalton','Itag Lamb Open'),('900002000109135','AVD741','White','Dalton','Itag Lamb Open'),('900002000109150','AVD742','White','Dalton','Itag Lamb Open'),('900002000109137','AVD743','White','Dalton','Itag Lamb Open'),('900002000109152','AVD744','White','Dalton','Itag Lamb Open'),('900044000052845','AVD745','White','Dalton','Itag Lamb Open'),('900002000109090','AVD746','White','Dalton','Itag Lamb Open'),('900044000052847','AVD747','White','Dalton','Itag Lamb Open'),('900002000109043','AVD748','White','Dalton','Itag Lamb Open'),('900044000052815','AVD749','White','Dalton','Itag Lamb Open'),('900044000052924','AVD750','White','Dalton','Itag Lamb Open'),('900044000052810','AVD751','White','Dalton','Itag Lamb Open'),('900044000052863','AVD752','White','Dalton','Itag Lamb Open'),('900044000052927','AVD753','White','Dalton','Itag Lamb Open'),('900044000052854','AVD754','White','Dalton','Itag Lamb Open'),('900044000052925','AVD755','White','Dalton','Itag Lamb Open'),('900002000109023','AVD756','White','Dalton','Itag Lamb Open'),('900044000052875','AVD757','White','Dalton','Itag Lamb Open'),('900002000109063','AVD758','White','Dalton','Itag Lamb Open'),('900044000052918','AVD759','White','Dalton','Itag Lamb Open'),('900044000052837','AVD760','White','Dalton','Itag Lamb Open'),('900044000052907','AVD761','White','Dalton','Itag Lamb Open'),('900044000052781','AVD762','White','Dalton','Itag Lamb Open'),('900044000052947','AVD763','White','Dalton','Itag Lamb Open'),('900044000052917','AVD764','White','Dalton','Itag Lamb Open'),('900002000109003','AVD765','White','Dalton','Itag Lamb Open'),('900044000052916','AVD766','White','Dalton','Itag Lamb Open'),('900044000052903','AVD767','White','Dalton','Itag Lamb Open'),('900002000109074','AVD768','White','Dalton','Itag Lamb Open'),('900044000052891','AVD769','White','Dalton','Itag Lamb Open'),('900044000052801','AVD770','White','Dalton','Itag Lamb Open'),('900044000052887','AVD771','White','Dalton','Itag Lamb Open'),('900044000052914','AVD772','White','Dalton','Itag Lamb Open'),('900044000052896','AVD773','White','Dalton','Itag Lamb Open'),('900002000109078','AVD774','White','Dalton','Itag Lamb Open'),('900044000052831','AVD775','White','Dalton','Itag Lamb Open'),('900044000052908','AVD776','White','Dalton','Itag Lamb Open'),('900044000052814','AVD777','White','Dalton','Itag Lamb Open'),('900044000052901','AVD778','White','Dalton','Itag Lamb Open'),('900002000109073','AVD779','White','Dalton','Itag Lamb Open'),('900002000109025','AVD780','White','Dalton','Itag Lamb Open'),('900044000052936','AVD781','White','Dalton','Itag Lamb Open'),('900044000052849','AVD782','White','Dalton','Itag Lamb Open'),('900002000109001','AVD783','White','Dalton','Itag Lamb Open'),('900044000052938','AVD784','White','Dalton','Itag Lamb Open'),('900002000109017','AVD785','White','Dalton','Itag Lamb Open'),('900002000109039','AVD786','White','Dalton','Itag Lamb Open'),('900002000109061','AVD787','White','Dalton','Itag Lamb Open'),('900044000052900','AVD788','White','Dalton','Itag Lamb Open'),('900002000109051','AVD789','White','Dalton','Itag Lamb Open'),('900002000109070','AVD790','White','Dalton','Itag Lamb Open'),('900002000109085','AVD791','White','Dalton','Itag Lamb Open'),('900002000109099','AVD792','White','Dalton','Itag Lamb Open'),('900002000109056','AVD793','White','Dalton','Itag Lamb Open'),('900002000109066','AVD794','White','Dalton','Itag Lamb Open'),('900002000109075','AVD795','White','Dalton','Itag Lamb Open'),('900002000109086','AVD796','White','Dalton','Itag Lamb Open'),('900002000109080','AVD797','White','Dalton','Itag Lamb Open'),('900002000109077','AVD798','White','Dalton','Itag Lamb Open'),('900002000109069','AVD799','White','Dalton','Itag Lamb Open'),('900002000109057','AVD800','White','Dalton','Itag Lamb Open'),('900002000109068','AVD801','White','Dalton','Itag Lamb Open'),('900002000109052','AVD802','White','Dalton','Itag Lamb Open'),('900002000109037','AVD803','White','Dalton','Itag Lamb Open'),('900002000109062','AVD804','White','Dalton','Itag Lamb Open'),('900002000109060','AVD805','White','Dalton','Itag Lamb Open'),('900002000109067','AVD806','White','Dalton','Itag Lamb Open'),('900002000109096','AVD807','White','Dalton','Itag Lamb Open'),('900002000109088','AVD808','White','Dalton','Itag Lamb Open'),('900002000109054','AVD809','White','Dalton','Itag Lamb Open'),('900002000109035','AVD810','White','Dalton','Itag Lamb Open'),('900002000109020','AVD811','White','Dalton','Itag Lamb Open'),('900002000109058','AVD812','White','Dalton','Itag Lamb Open'),('900002000109084','AVD813','White','Dalton','Itag Lamb Open'),('900002000109027','AVD814','White','Dalton','Itag Lamb Open'),('900002000109076','AVD815','White','Dalton','Itag Lamb Open'),('900002000109087','AVD816','White','Dalton','Itag Lamb Open'),('900002000109095','AVD817','White','Dalton','Itag Lamb Open'),('900002000109021','AVD818','White','Dalton','Itag Lamb Open'),('900002000109091','AVD819','White','Dalton','Itag Lamb Open'),('900002000109029','AVD820','White','Dalton','Itag Lamb Open'),('900002000109053','AVD821','White','Dalton','Itag Lamb Open'),('900002000109007','AVD822','White','Dalton','Itag Lamb Open'),('900044000052920','AVD823','White','Dalton','Itag Lamb Open'),('900002000109094','AVD824','White','Dalton','Itag Lamb Open'),('900002000109002','AVD825','White','Dalton','Itag Lamb Open'),('900002000109083','AVD826','White','Dalton','Itag Lamb Open'),('900002000109082','AVD827','White','Dalton','Itag Lamb Open'),('900002000109065','AVD828','White','Dalton','Itag Lamb Open'),('900044000052933','AVD829','White','Dalton','Itag Lamb Open'),('900002000109092','AVD830','White','Dalton','Itag Lamb Open'),('900002000109098','AVD831','White','Dalton','Itag Lamb Open'),('900002000109064','AVD832','White','Dalton','Itag Lamb Open'),('900002000109018','AVD833','White','Dalton','Itag Lamb Open'),('900002000109071','AVD834','White','Dalton','Itag Lamb Open'),('900002000109100','AVD835','White','Dalton','Itag Lamb Open'),('900002000109019','AVD836','White','Dalton','Itag Lamb Open'),('900002000109032','AVD837','White','Dalton','Itag Lamb Open'),('900002000109093','AVD838','White','Dalton','Itag Lamb Open'),('900002000109022','AVD839','White','Dalton','Itag Lamb Open'),('900002000109089','AVD840','White','Dalton','Itag Lamb Open'),('900002000109097','AVD841','White','Dalton','Itag Lamb Open'),('900002000109072','AVD842','White','Dalton','Itag Lamb Open'),('900002000109010','AVD843','White','Dalton','Itag Lamb Open'),('900002000109024','AVD844','White','Dalton','Itag Lamb Open'),('900002000109013','AVD845','White','Dalton','Itag Lamb Open'),('900002000109009','AVD846','White','Dalton','Itag Lamb Open'),('900002000109014','AVD847','White','Dalton','Itag Lamb Open'),('900002000109005','AVD848','White','Dalton','Itag Lamb Open'),('900002000109030','AVD849','White','Dalton','Itag Lamb Open'),('900002000109041','AVD850','White','Dalton','Itag Lamb Open'),('900002000109046','AVD851','White','Dalton','Itag Lamb Open'),('900002000109016','AVD852','White','Dalton','Itag Lamb Open'),('900002000109040','AVD853','White','Dalton','Itag Lamb Open'),('900002000109006','AVD854','White','Dalton','Itag Lamb Open'),('900002000109038','AVD855','White','Dalton','Itag Lamb Open'),('900002000109015','AVD856','White','Dalton','Itag Lamb Open'),('900002000109008','AVD857','White','Dalton','Itag Lamb Open'),('900002000109044','AVD858','White','Dalton','Itag Lamb Open'),('900002000109031','AVD859','White','Dalton','Itag Lamb Open'),('900002000109026','AVD860','White','Dalton','Itag Lamb Open'),('900002000109036','AVD861','White','Dalton','Itag Lamb Open'),('900002000109048','AVD862','White','Dalton','Itag Lamb Open'),('900002000109047','AVD863','White','Dalton','Itag Lamb Open'),('900002000109050','AVD864','White','Dalton','Itag Lamb Open'),('900002000109011','AVD865','White','Dalton','Itag Lamb Open'),('900002000109079','AVD866','White','Dalton','Itag Lamb Open'),('900002000109033','AVD867','White','Dalton','Itag Lamb Open'),('900002000109081','AVD868','White','Dalton','Itag Lamb Open'),('900002000109012','AVD869','White','Dalton','Itag Lamb Open'),('900002000109004','AVD870','White','Dalton','Itag Lamb Open'),('900002000109055','AVD871','White','Dalton','Itag Lamb Open'),('900002000109049','AVD872','White','Dalton','Itag Lamb Open'),('900002000109045','AVD873','White','Dalton','Itag Lamb Open'),('900002000109034','AVD874','White','Dalton','Itag Lamb Open'),('900044000052834','AVD875','White','Dalton','Itag Lamb Open'),('900044000052866','AVD876','White','Dalton','Itag Lamb Open'),('900044000052946','AVD877','White','Dalton','Itag Lamb Open'),('900044000052934','AVD878','White','Dalton','Itag Lamb Open'),('900044000052865','AVD879','White','Dalton','Itag Lamb Open'),('900044000052871','AVD880','White','Dalton','Itag Lamb Open'),('900044000052826','AVD881','White','Dalton','Itag Lamb Open'),('900044000052864','AVD882','White','Dalton','Itag Lamb Open'),('900044000052944','AVD883','White','Dalton','Itag Lamb Open'),('900044000052773','AVD884','White','Dalton','Itag Lamb Open'),('900044000052898','AVD885','White','Dalton','Itag Lamb Open'),('900044000052765','AVD886','White','Dalton','Itag Lamb Open'),('900044000052904','AVD887','White','Dalton','Itag Lamb Open'),('900044000052919','AVD888','White','Dalton','Itag Lamb Open'),('900044000052882','AVD889','White','Dalton','Itag Lamb Open'),('900044000052873','AVD890','White','Dalton','Itag Lamb Open'),('900044000052915','AVD891','White','Dalton','Itag Lamb Open'),('900044000052777','AVD892','White','Dalton','Itag Lamb Open'),('900044000052780','AVD893','White','Dalton','Itag Lamb Open'),('900044000052880','AVD894','White','Dalton','Itag Lamb Open'),('900044000052848','AVD895','White','Dalton','Itag Lamb Open'),('900044000052869','AVD896','White','Dalton','Itag Lamb Open'),('900044000052828','AVD897','White','Dalton','Itag Lamb Open'),('900044000052877','AVD898','White','Dalton','Itag Lamb Open'),('900044000052860','AVD899','White','Dalton','Itag Lamb Open'),('900044000052853','AVD900','White','Dalton','Itag Lamb Open'),('900044000052931','AVD901','White','Dalton','Itag Lamb Open'),('900044000052895','AVD902','White','Dalton','Itag Lamb Open'),('900044000052879','AVD903','White','Dalton','Itag Lamb Open'),('900044000052841','AVD904','White','Dalton','Itag Lamb Open'),('900044000052861','AVD905','White','Dalton','Itag Lamb Open'),('900044000052786','AVD906','White','Dalton','Itag Lamb Open'),('900044000052883','AVD907','White','Dalton','Itag Lamb Open'),('900044000052876','AVD908','White','Dalton','Itag Lamb Open'),('900044000052862','AVD909','White','Dalton','Itag Lamb Open'),('900044000052858','AVD910','White','Dalton','Itag Lamb Open'),('900044000052794','AVD911','White','Dalton','Itag Lamb Open'),('900044000052783','AVD912','White','Dalton','Itag Lamb Open'),('900044000052893','AVD913','White','Dalton','Itag Lamb Open'),('900044000052784','AVD914','White','Dalton','Itag Lamb Open'),('900044000052787','AVD915','White','Dalton','Itag Lamb Open'),('900044000052859','AVD916','White','Dalton','Itag Lamb Open'),('900044000052897','AVD917','White','Dalton','Itag Lamb Open'),('900044000052851','AVD918','White','Dalton','Itag Lamb Open'),('900044000052807','AVD919','White','Dalton','Itag Lamb Open'),('900044000052839','AVD920','White','Dalton','Itag Lamb Open'),('900044000052813','AVD921','White','Dalton','Itag Lamb Open'),('900044000052821','AVD922','White','Dalton','Itag Lamb Open'),('900044000052868','AVD923','White','Dalton','Itag Lamb Open'),('900044000052818','AVD924','White','Dalton','Itag Lamb Open'),('900044000052791','AVD925','White','Dalton','Itag Lamb Open'),('900044000052888','AVD926','White','Dalton','Itag Lamb Open'),('900044000052940','AVD927','White','Dalton','Itag Lamb Open'),('900044000052778','AVD928','White','Dalton','Itag Lamb Open'),('900044000052825','AVD929','White','Dalton','Itag Lamb Open'),('900044000052874','AVD930','White','Dalton','Itag Lamb Open'),('900044000052948','AVD931','White','Dalton','Itag Lamb Open'),('900044000052749','AVD932','White','Dalton','Itag Lamb Open'),('900044000052909','AVD933','White','Dalton','Itag Lamb Open'),('900044000052785','AVD934','White','Dalton','Itag Lamb Open'),('900044000052774','AVD935','White','Dalton','Itag Lamb Open'),('900044000052782','AVD936','White','Dalton','Itag Lamb Open'),('900044000052878','AVD937','White','Dalton','Itag Lamb Open'),('900044000052870','AVD938','White','Dalton','Itag Lamb Open'),('900044000052829','AVD939','White','Dalton','Itag Lamb Open'),('900044000052827','AVD940','White','Dalton','Itag Lamb Open'),('900044000052819','AVD941','White','Dalton','Itag Lamb Open'),('900044000052796','AVD942','White','Dalton','Itag Lamb Open'),('900044000052751','AVD943','White','Dalton','Itag Lamb Open'),('900044000052758','AVD944','White','Dalton','Itag Lamb Open'),('900044000052757','AVD945','White','Dalton','Itag Lamb Open'),('900044000052792','AVD946','White','Dalton','Itag Lamb Open'),('900044000052793','AVD947','White','Dalton','Itag Lamb Open'),('900044000052832','AVD948','White','Dalton','Itag Lamb Open'),('900044000052763','AVD949','White','Dalton','Itag Lamb Open'),('900044000052840','AVD950','White','Dalton','Itag Lamb Open'),('900044000052809','AVD951','White','Dalton','Itag Lamb Open'),('900044000052803','AVD952','White','Dalton','Itag Lamb Open'),('900044000052779','AVD953','White','Dalton','Itag Lamb Open'),('900044000052752','AVD954','White','Dalton','Itag Lamb Open'),('900044000052844','AVD955','White','Dalton','Itag Lamb Open'),('900044000052843','AVD956','White','Dalton','Itag Lamb Open'),('900044000052802','AVD957','White','Dalton','Itag Lamb Open'),('900044000052800','AVD958','White','Dalton','Itag Lamb Open'),('900044000052811','AVD959','White','Dalton','Itag Lamb Open'),('900044000052812','AVD960','White','Dalton','Itag Lamb Open'),('900044000052838','AVD961','White','Dalton','Itag Lamb Open'),('900044000052835','AVD962','White','Dalton','Itag Lamb Open'),('900044000052820','AVD963','White','Dalton','Itag Lamb Open'),('900044000052768','AVD964','White','Dalton','Itag Lamb Open'),('900044000052771','AVD965','White','Dalton','Itag Lamb Open'),('900044000052790','AVD966','White','Dalton','Itag Lamb Open'),('900044000052797','AVD967','White','Dalton','Itag Lamb Open'),('900044000052755','AVD968','White','Dalton','Itag Lamb Open'),('900044000052833','AVD969','White','Dalton','Itag Lamb Open'),('900044000052824','AVD970','White','Dalton','Itag Lamb Open'),('900044000052817','AVD971','White','Dalton','Itag Lamb Open'),('900044000052799','AVD972','White','Dalton','Itag Lamb Open'),('900044000052761','AVD973','White','Dalton','Itag Lamb Open'),('900044000052795','AVD974','White','Dalton','Itag Lamb Open'),('900044000052769','AVD975','White','Dalton','Itag Lamb Open'),('900044000052846','AVD976','White','Dalton','Itag Lamb Open'),('900044000052775','AVD977','White','Dalton','Itag Lamb Open'),('900044000052830','AVD978','White','Dalton','Itag Lamb Open'),('900044000052760','AVD979','White','Dalton','Itag Lamb Open'),('900044000052767','AVD980','White','Dalton','Itag Lamb Open'),('900044000052750','AVD981','White','Dalton','Itag Lamb Open'),('900044000052805','AVD982','White','Dalton','Itag Lamb Open'),('900044000052766','AVD983','White','Dalton','Itag Lamb Open'),('900044000052798','AVD984','White','Dalton','Itag Lamb Open'),('900044000052823','AVD985','White','Dalton','Itag Lamb Open'),('900044000052789','AVD986','White','Dalton','Itag Lamb Open'),('900044000052759','AVD987','White','Dalton','Itag Lamb Open'),('900044000052764','AVD988','White','Dalton','Itag Lamb Open'),('900044000052772','AVD989','White','Dalton','Itag Lamb Open'),('900044000052808','AVD990','White','Dalton','Itag Lamb Open'),('900044000052762','AVD991','White','Dalton','Itag Lamb Open'),('900044000052816','AVD992','White','Dalton','Itag Lamb Open'),('900044000052754','AVD993','White','Dalton','Itag Lamb Open'),('900044000052753','AVD994','White','Dalton','Itag Lamb Open'),('900044000052776','AVD995','White','Dalton','Itag Lamb Open'),('900044000054805','AVD996','White','Dalton','Itag Lamb Open'),('900044000054840','AVD997','White','Dalton','Itag Lamb Open'),('900002000098591','AVD998','White','Dalton','Itag Lamb Open'),('900044000054829','AVD999','White','Dalton','Itag Lamb Open'),('966000000012655','AVD001','Yellow','Ritchey','RD2000 EID'),('966000000012692','AVD002','Yellow','Ritchey','RD2000 EID'),('966000000012700','AVD003','Yellow','Ritchey','RD2000 EID'),('966000000012699','AVD004','Yellow','Ritchey','RD2000 EID'),('966000000012661','AVD005','Yellow','Ritchey','RD2000 EID'),('966000000012623','AVD006','Yellow','Ritchey','RD2000 EID'),('966000000012624','AVD007','Yellow','Ritchey','RD2000 EID'),('966000000012662','AVD008','Yellow','Ritchey','RD2000 EID'),('966000000012631','AVD009','Yellow','Ritchey','RD2000 EID'),('966000000012613','AVD010','Yellow','Ritchey','RD2000 EID'),('966000000012605','AVD011','Yellow','Ritchey','RD2000 EID'),('966000000012666','AVD012','Yellow','Ritchey','RD2000 EID'),('966000000012663','AVD013','Yellow','Ritchey','RD2000 EID'),('966000000012686','AVD014','Yellow','Ritchey','RD2000 EID'),('966000000012654','AVD015','Yellow','Ritchey','RD2000 EID'),('966000000012619','AVD016','Yellow','Ritchey','RD2000 EID'),('966000000012626','AVD017','Yellow','Ritchey','RD2000 EID'),('966000000012638','AVD018','Yellow','Ritchey','RD2000 EID'),('966000000012606','AVD019','Yellow','Ritchey','RD2000 EID'),('966000000012625','AVD020','Yellow','Ritchey','RD2000 EID'),('966000000019163','AVD021','Yellow','Ritchey','RD2000 EID'),('966000000019136','AVD022','Yellow','Ritchey','RD2000 EID'),('966000000019126','AVD023','Yellow','Ritchey','RD2000 EID'),('966000000019112','AVD024','Yellow','Ritchey','RD2000 EID'),('966000000019114','AVD025','Yellow','Ritchey','RD2000 EID'),('966000000019141','AVD026','Yellow','Ritchey','RD2000 EID'),('966000000019146','AVD027','Yellow','Ritchey','RD2000 EID'),('966000000019123','AVD028','Yellow','Ritchey','RD2000 EID'),('966000000019166','AVD029','Yellow','Ritchey','RD2000 EID'),('966000000019103','AVD030','Yellow','Ritchey','RD2000 EID'),('966000000019148','AVD031','Yellow','Ritchey','RD2000 EID'),('966000000019160','AVD032','Yellow','Ritchey','RD2000 EID'),('966000000019133','AVD033','Yellow','Ritchey','RD2000 EID'),('966000000019113','AVD034','Yellow','Ritchey','RD2000 EID'),('966000000019111','AVD035','Yellow','Ritchey','RD2000 EID'),('966000000019102','AVD036','Yellow','Ritchey','RD2000 EID'),('966000000019129','AVD037','Yellow','Ritchey','RD2000 EID'),('966000000019118','AVD038','Yellow','Ritchey','RD2000 EID'),('966000000019108','AVD039','Yellow','Ritchey','RD2000 EID'),('966000000019144','AVD040','Yellow','Ritchey','RD2000 EID'),('966000000019142','AVD041','Yellow','Ritchey','RD2000 EID'),('966000000019134','AVD042','Yellow','Ritchey','RD2000 EID'),('966000000019106','AVD043','Yellow','Ritchey','RD2000 EID'),('966000000019159','AVD044','Yellow','Ritchey','RD2000 EID'),('966000000019139','AVD045','Yellow','Ritchey','RD2000 EID'),('966000000019151','AVD046','Yellow','Ritchey','RD2000 EID'),('966000000019127','AVD047','Yellow','Ritchey','RD2000 EID'),('966000000019147','AVD048','Yellow','Ritchey','RD2000 EID'),('966000000019182','AVD049','Yellow','Ritchey','RD2000 EID'),('966000000019164','AVD050','Yellow','Ritchey','RD2000 EID'),('966000000019170','AVD051','Yellow','Ritchey','RD2000 EID'),('966000000019115','AVD052','Yellow','Ritchey','RD2000 EID'),('966000000019135','AVD053','Yellow','Ritchey','RD2000 EID'),('966000000019193','AVD054','Yellow','Ritchey','RD2000 EID'),('966000000019120','AVD055','Yellow','Ritchey','RD2000 EID'),('966000000019117','AVD056','Yellow','Ritchey','RD2000 EID'),('966000000019183','AVD057','Yellow','Ritchey','RD2000 EID'),('966000000019176','AVD058','Yellow','Ritchey','RD2000 EID'),('966000000019157','AVD059','Yellow','Ritchey','RD2000 EID'),('966000000019105','AVD060','Yellow','Ritchey','RD2000 EID'),('966000000012642','AVD061','Yellow','Ritchey','RD2000 EID'),('966000000012641','AVD062','Yellow','Ritchey','RD2000 EID'),('966000000012633','AVD063','Yellow','Ritchey','RD2000 EID'),('966000000012627','AVD064','Yellow','Ritchey','RD2000 EID'),('966000000012650','AVD065','Yellow','Ritchey','RD2000 EID'),('966000000012611','AVD066','Yellow','Ritchey','RD2000 EID'),('966000000012621','AVD067','Yellow','Ritchey','RD2000 EID'),('966000000012603','AVD068','Yellow','Ritchey','RD2000 EID'),('966000000012622','AVD069','Yellow','Ritchey','RD2000 EID'),('966000000012608','AVD070','Yellow','Ritchey','RD2000 EID'),('966000000012669','AVD071','Yellow','Ritchey','RD2000 EID'),('966000000012634','AVD072','Yellow','Ritchey','RD2000 EID'),('966000000012609','AVD073','Yellow','Ritchey','RD2000 EID'),('966000000012629','AVD074','Yellow','Ritchey','RD2000 EID'),('966000000012646','AVD075','Yellow','Ritchey','RD2000 EID'),('966000000012656','AVD076','Yellow','Ritchey','RD2000 EID'),('966000000012615','AVD077','Yellow','Ritchey','RD2000 EID'),('966000000012660','AVD078','Yellow','Ritchey','RD2000 EID'),('966000000012647','AVD079','Yellow','Ritchey','RD2000 EID'),('966000000012644','AVD080','Yellow','Ritchey','RD2000 EID'),('966000000019130','AVD081','Yellow','Ritchey','RD2000 EID'),('966000000019185','AVD082','Yellow','Ritchey','RD2000 EID'),('966000000019179','AVD083','Yellow','Ritchey','RD2000 EID'),('966000000019172','AVD084','Yellow','Ritchey','RD2000 EID'),('966000000019173','AVD085','Yellow','Ritchey','RD2000 EID'),('966000000019195','AVD086','Yellow','Ritchey','RD2000 EID'),('966000000019175','AVD087','Yellow','Ritchey','RD2000 EID'),('966000000019196','AVD088','Yellow','Ritchey','RD2000 EID'),('966000000019124','AVD089','Yellow','Ritchey','RD2000 EID'),('966000000019125','AVD090','Yellow','Ritchey','RD2000 EID'),('966000000019200','AVD091','Yellow','Ritchey','RD2000 EID'),('966000000019167','AVD092','Yellow','Ritchey','RD2000 EID'),('966000000019199','AVD093','Yellow','Ritchey','RD2000 EID'),('966000000019169','AVD094','Yellow','Ritchey','RD2000 EID'),('966000000019162','AVD095','Yellow','Ritchey','RD2000 EID'),('966000000019178','AVD096','Yellow','Ritchey','RD2000 EID'),('966000000019189','AVD097','Yellow','Ritchey','RD2000 EID'),('966000000019180','AVD098','Yellow','Ritchey','RD2000 EID'),('966000000019190','AVD099','Yellow','Ritchey','RD2000 EID'),('966000000019155','AVD100','Yellow','Ritchey','RD2000 EID'),('966000000019171','AVD101','Yellow','Ritchey','RD2000 EID'),('966000000019191','AVD102','Yellow','Ritchey','RD2000 EID'),('966000000019194','AVD103','Yellow','Ritchey','RD2000 EID'),('966000000019198','AVD104','Yellow','Ritchey','RD2000 EID'),('966000000019197','AVD105','Yellow','Ritchey','RD2000 EID'),('966000000019177','AVD106','Yellow','Ritchey','RD2000 EID'),('966000000019153','AVD107','Yellow','Ritchey','RD2000 EID'),('966000000019223','AVD108','Yellow','Ritchey','RD2000 EID'),('966000000019302','AVD109','Yellow','Ritchey','RD2000 EID'),('966000000019248','AVD110','Yellow','Ritchey','RD2000 EID'),('966000000019204','AVD111','Yellow','Ritchey','RD2000 EID'),('966000000019354','AVD112','Yellow','Ritchey','RD2000 EID'),('966000000019281','AVD113','Yellow','Ritchey','RD2000 EID'),('966000000019344','AVD114','Yellow','Ritchey','RD2000 EID'),('966000000019288','AVD115','Yellow','Ritchey','RD2000 EID'),('966000000019215','AVD116','Yellow','Ritchey','RD2000 EID'),('966000000019237','AVD117','Yellow','Ritchey','RD2000 EID'),('966000000019284','AVD118','Yellow','Ritchey','RD2000 EID'),('966000000019205','AVD119','Yellow','Ritchey','RD2000 EID'),('966000000019273','AVD120','Yellow','Ritchey','RD2000 EID'),('966000000019255','AVD121','Yellow','Ritchey','RD2000 EID'),('966000000019381','AVD122','Yellow','Ritchey','RD2000 EID'),('966000000019218','AVD123','Yellow','Ritchey','RD2000 EID'),('966000000019318','AVD124','Yellow','Ritchey','RD2000 EID'),('966000000019257','AVD125','Yellow','Ritchey','RD2000 EID'),('966000000019225','AVD126','Yellow','Ritchey','RD2000 EID'),('966000000019319','AVD127','Yellow','Ritchey','RD2000 EID'),('966000000019264','AVD128','Yellow','Ritchey','RD2000 EID'),('966000000019366','AVD129','Yellow','Ritchey','RD2000 EID'),('966000000019245','AVD130','Yellow','Ritchey','RD2000 EID'),('966000000019235','AVD131','Yellow','Ritchey','RD2000 EID'),('966000000019309','AVD132','Yellow','Ritchey','RD2000 EID'),('966000000019374','AVD133','Yellow','Ritchey','RD2000 EID'),('966000000019272','AVD134','Yellow','Ritchey','RD2000 EID'),('966000000019263','AVD135','Yellow','Ritchey','RD2000 EID'),('966000000019375','AVD136','Yellow','Ritchey','RD2000 EID'),('966000000019270','AVD137','Yellow','Ritchey','RD2000 EID'),('966000000019361','AVD138','Yellow','Ritchey','RD2000 EID'),('966000000019321','AVD139','Yellow','Ritchey','RD2000 EID'),('966000000019266','AVD140','Yellow','Ritchey','RD2000 EID'),('966000000012612','AVD141','Yellow','Ritchey','RD2000 EID'),('966000000012664','AVD142','Yellow','Ritchey','RD2000 EID'),('966000000012635','AVD143','Yellow','Ritchey','RD2000 EID'),('966000000012637','AVD144','Yellow','Ritchey','RD2000 EID'),('966000000012636','AVD145','Yellow','Ritchey','RD2000 EID'),('966000000012604','AVD146','Yellow','Ritchey','RD2000 EID'),('966000000012676','AVD147','Yellow','Ritchey','RD2000 EID'),('966000000012620','AVD148','Yellow','Ritchey','RD2000 EID'),('966000000012607','AVD149','Yellow','Ritchey','RD2000 EID'),('966000000012628','AVD150','Yellow','Ritchey','RD2000 EID'),('966000000012645','AVD151','Yellow','Ritchey','RD2000 EID'),('966000000012640','AVD152','Yellow','Ritchey','RD2000 EID'),('966000000012648','AVD153','Yellow','Ritchey','RD2000 EID'),('966000000012632','AVD154','Yellow','Ritchey','RD2000 EID'),('966000000012602','AVD155','Yellow','Ritchey','RD2000 EID'),('966000000012668','AVD156','Yellow','Ritchey','RD2000 EID'),('966000000012643','AVD157','Yellow','Ritchey','RD2000 EID'),('966000000012649','AVD158','Yellow','Ritchey','RD2000 EID'),('966000000012617','AVD159','Yellow','Ritchey','RD2000 EID'),('966000000012614','AVD160','Yellow','Ritchey','RD2000 EID'),('966000000012672','AVD161','Yellow','Ritchey','RD2000 EID'),('966000000012681','AVD162','Yellow','Ritchey','RD2000 EID'),('966000000012630','AVD163','Yellow','Ritchey','RD2000 EID'),('966000000012616','AVD164','Yellow','Ritchey','RD2000 EID'),('966000000012610','AVD165','Yellow','Ritchey','RD2000 EID'),('966000000012618','AVD166','Yellow','Ritchey','RD2000 EID'),('966000000012601','AVD167','Yellow','Ritchey','RD2000 EID'),('966000000019137','AVD168','Yellow','Ritchey','RD2000 EID'),('966000000019149','AVD169','Yellow','Ritchey','RD2000 EID'),('966000000019145','AVD170','Yellow','Ritchey','RD2000 EID'),('966000000019131','AVD171','Yellow','Ritchey','RD2000 EID'),('966000000019107','AVD172','Yellow','Ritchey','RD2000 EID'),('966000000019138','AVD173','Yellow','Ritchey','RD2000 EID'),('966000000019143','AVD174','Yellow','Ritchey','RD2000 EID'),('966000000019116','AVD175','Yellow','Ritchey','RD2000 EID'),('966000000019109','AVD176','Yellow','Ritchey','RD2000 EID'),('966000000019132','AVD177','Yellow','Ritchey','RD2000 EID'),('966000000019121','AVD178','Yellow','Ritchey','RD2000 EID'),('966000000019128','AVD179','Yellow','Ritchey','RD2000 EID'),('966000000019140','AVD180','Yellow','Ritchey','RD2000 EID'),('966000000019187','AVD181','Yellow','Ritchey','RD2000 EID'),('966000000019150','AVD182','Yellow','Ritchey','RD2000 EID'),('966000000019152','AVD183','Yellow','Ritchey','RD2000 EID'),('966000000019119','AVD184','Yellow','Ritchey','RD2000 EID'),('966000000019165','AVD185','Yellow','Ritchey','RD2000 EID'),('966000000019161','AVD186','Yellow','Ritchey','RD2000 EID'),('966000000019104','AVD187','Yellow','Ritchey','RD2000 EID'),('966000000019184','AVD188','Yellow','Ritchey','RD2000 EID'),('966000000019181','AVD189','Yellow','Ritchey','RD2000 EID'),('966000000019158','AVD190','Yellow','Ritchey','RD2000 EID'),('966000000019110','AVD191','Yellow','Ritchey','RD2000 EID'),('966000000019174','AVD192','Yellow','Ritchey','RD2000 EID'),('966000000019154','AVD193','Yellow','Ritchey','RD2000 EID'),('966000000019192','AVD194','Yellow','Ritchey','RD2000 EID'),('966000000019101','AVD195','Yellow','Ritchey','RD2000 EID'),('966000000019156','AVD196','Yellow','Ritchey','RD2000 EID'),('966000000019122','AVD197','Yellow','Ritchey','RD2000 EID'),('966000000019168','AVD198','Yellow','Ritchey','RD2000 EID'),('966000000019186','AVD199','Yellow','Ritchey','RD2000 EID'),('966000000019188','AVD200','Yellow','Ritchey','RD2000 EID');
/*!40000 ALTER TABLE `tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Final view structure for view `active_animals`
--

/*!50001 DROP TABLE `active_animals`*/;
/*!50001 DROP VIEW IF EXISTS `active_animals`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_animals` AS select `a`.`id` AS `id`,`a`.`tag` AS `tag`,`a`.`date_of_birth` AS `date_of_birth`,`a`.`sex` AS `sex`,`a`.`species` AS `species`,`a`.`owner` AS `owner`,`a`.`location` AS `location`,`m`.`id` AS `m_id`,`m`.`animal` AS `animal`,`m`.`approximate_age` AS `approximate_age`,`m`.`measure_time` AS `measure_time`,`m`.`comment` AS `comment` from (`animals` `a` join `animal_measures` `m` on((`a`.`tag` = `m`.`animal`))) where (not(`a`.`tag` in (select `tag_replacements`.`replaces` AS `replaces` from `tag_replacements`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `active_samples`
--

/*!50001 DROP TABLE `active_samples`*/;
/*!50001 DROP VIEW IF EXISTS `active_samples`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_samples` AS select `a`.`id` AS `id`,concat(`a`.`prefix`,`a`.`barcode`) AS `barcode`,`a`.`tag_read` AS `tag_read`,`a`.`sample_time` AS `sample_time`,`a`.`latitude` AS `latitude`,`a`.`longtitude` AS `longtitude`,`a`.`altitude` AS `altitude`,`a`.`hdop` AS `hdop`,`a`.`satellites` AS `satellites`,`a`.`comment` AS `comment`,`a`.`raw_data` AS `raw_data` from `samples` `a` where (not(concat(`a`.`prefix`,`a`.`barcode`) in (select concat(`deleted_samples`.`prefix`,`deleted_samples`.`barcode`) AS `concat(prefix, barcode)` from `deleted_samples`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `active_tags`
--

/*!50001 DROP TABLE `active_tags`*/;
/*!50001 DROP VIEW IF EXISTS `active_tags`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `active_tags` AS select `tags`.`rfid` AS `rfid`,`tags`.`label` AS `label`,`tags`.`color` AS `color`,`tags`.`supplier` AS `supplier`,`tags`.`type` AS `type` from `tags` where (not(`tags`.`label` in (select `tag_replacements`.`replaces` AS `replaces` from `tag_replacements`))) union select `tag_replacements`.`rfid` AS `rfid`,`tag_replacements`.`label` AS `label`,`tag_replacements`.`color` AS `color`,`tag_replacements`.`supplier` AS `supplier`,`tag_replacements`.`type` AS `type` from `tag_replacements` where (not(`tag_replacements`.`label` in (select `tag_replacements`.`replaces` AS `replaces` from `tag_replacements`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `export_animals`
--

/*!50001 DROP TABLE `export_animals`*/;
/*!50001 DROP VIEW IF EXISTS `export_animals`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `export_animals` AS select `a`.`id` AS `id`,`a`.`tag` AS `animal_id`,`a`.`species` AS `organism`,`b`.`approximate_age` AS `age`,`a`.`sex` AS `sex`,`c`.`replaces` AS `prev_tag`,`a`.`location` AS `location`,`b`.`comment` AS `comments` from ((`animals` `a` join `animal_measures` `b` on((`a`.`tag` = `b`.`animal`))) left join `tag_replacements` `c` on((`c`.`label` = `a`.`tag`))) where (not(`a`.`tag` in (select `tag_replacements`.`replaces` AS `replaces` from `tag_replacements`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `export_samples`
--

/*!50001 DROP TABLE `export_samples`*/;
/*!50001 DROP VIEW IF EXISTS `export_samples`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `export_samples` AS select `a`.`id` AS `id`,concat(`a`.`prefix`,`a`.`barcode`) AS `label`,`c`.`id` AS `animal_id`,`a`.`latitude` AS `latitude`,`a`.`longtitude` AS `longtitude`,`a`.`altitude` AS `altitude`,`a`.`sample_time` AS `timestamp`,`a`.`comment` AS `comments` from ((`samples` `a` join `tag_reads` `b` on((`a`.`tag_read` = `b`.`id`))) join `active_animals` `c` on((`b`.`rfid` = `c`.`tag`))) where (not(concat(`a`.`prefix`,`a`.`barcode`) in (select concat(`deleted_samples`.`prefix`,`deleted_samples`.`barcode`) AS `CONCAT(prefix, barcode)` from `deleted_samples`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `recently_sampled`
--

/*!50001 DROP TABLE `recently_sampled`*/;
/*!50001 DROP VIEW IF EXISTS `recently_sampled`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `recently_sampled` AS select `a`.`tag` AS `tag`,`a`.`sex` AS `sex`,`a`.`owner` AS `owner`,`a`.`location` AS `location`,`b`.`rfid` AS `sampled` from (`active_animals` `a` left join `sampled_reads` `b` on((`a`.`tag` = `b`.`rfid`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `sampled_reads`
--

/*!50001 DROP TABLE `sampled_reads`*/;
/*!50001 DROP VIEW IF EXISTS `sampled_reads`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = latin1 */;
/*!50001 SET character_set_results     = latin1 */;
/*!50001 SET collation_connection      = latin1_swedish_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `sampled_reads` AS select `tag_reads`.`id` AS `id`,`tag_reads`.`rfid` AS `rfid` from `tag_reads` where `tag_reads`.`id` in (select `active_samples`.`tag_read` AS `tag_read` from `active_samples` where ((to_days(now()) - to_days(`active_samples`.`sample_time`)) < 1)) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2010-05-21 11:15:37

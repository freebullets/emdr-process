DROP TABLE IF EXISTS `marketOrders`;
CREATE TABLE `marketOrders` (
  `orderID` bigint(11) NOT NULL,
  `generationDate` datetime NOT NULL,
  `issueDate` datetime NOT NULL,
  `typeID` int(11) NOT NULL,
  `price` double NOT NULL,
  `volEntered` int(11) NOT NULL,
  `volRemaining` int(11) NOT NULL,
  `range` int(11) NOT NULL,
  `duration` int(11) NOT NULL,
  `minVolume` int(11) NOT NULL,
  `bid` tinyint(1) NOT NULL,
  `stationID` int(11) NOT NULL,
  `solarSystemID` int(11) NOT NULL,
  `regionID` int(11) NOT NULL,
  PRIMARY KEY (`orderID`),
  KEY `idx_region` (`regionID`, `typeID`, `bid`, `price`),
  KEY `idx_station` (`stationID`, `typeID`, `bid`, `price`),
  KEY `idx_order` (`regionID`, `typeID`, `orderID`),
  KEY `idx_typeID` (`typeID`),
--  KEY `generationDate` (`generationDate`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `marketHistory` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `regionID` int(11) NOT NULL,
  `date` date NOT NULL,
  `typeID` int(11) NOT NULL,
  `price_low` double NOT NULL,
  `price_high` double NOT NULL,
  `price_average` double NOT NULL,
  `quantity` bigint(20) NOT NULL,
  `num_orders` bigint(20) NOT NULL,
  `created` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_type` (`typeID`, `regionID`, `date`),
) ENGINE=InnoDB AUTO_INCREMENT=40999441 DEFAULT CHARSET=latin1

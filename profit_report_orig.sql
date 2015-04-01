SELECT
  `typeName` AS `name`, 
  COALESCE(`attrib`.`valueInt`, `attrib`.`valueFloat`) AS `meta`, 
  `history`.`volume` AS `volume`, 
  `sell`.`price` AS `sell_price`, 
  `buy`.`price` AS `buy_price`, 
  (`sell`.`price` * 0.985 - `buy`.`price` * 1.025) AS `margin`, 
  ((`sell`.`price` * 0.985 - `buy`.`price` * 1.025) * `history`.`volume`) AS `daily_movement`
FROM `invTypes`
INNER JOIN `dgmTypeAttributes` AS `attrib`
  ON `attrib`.`typeID` = `invTypes`.`typeID`
  AND `attrib`.`attributeID` = 633
  AND (`attrib`.`valueInt` = 4 OR `attrib`.`valueFloat` = 4)
-- INNER JOIN `invMetaTypes`
--   ON `invMetaTypes`.`typeID` = `invTypes`.`typeID`
--   AND `invMetaTypes`.`metaGroupID` = 1
INNER JOIN (
  SELECT 
    SUM(`quantity`)/30 AS `volume`,
    `type_id`
  FROM `items_history`
  WHERE `date` >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
  GROUP BY `type_id`
) AS `history`
  ON `history`.`type_id` = `invTypes`.`typeID`
INNER JOIN (
  SELECT 
    MIN(`price`) AS `price`, 
    `typeID`
  FROM `marketOrdersMem`
  WHERE `marketOrdersMem`.`stationID` = 60003760
  AND `marketOrdersMem`.`bid`=0
  GROUP BY `typeID`
) AS `sell`
  ON `sell`.`typeID` = `invTypes`.`typeID`
INNER JOIN (
  SELECT 
    MAX(`price`) AS `price`, 
    `typeID`
  FROM `marketOrdersMem`
  WHERE `marketOrdersMem`.`stationID` = 60003760
  AND `marketOrdersMem`.`bid`=1
  GROUP BY `typeID`
) AS `buy`
  ON `buy`.`typeID` = `invTypes`.`typeID`
ORDER BY `daily_movement` DESC
LIMIT 20
-- INTO OUTFILE '/srv/http/output.csv'
-- FIELDS TERMINATED BY ','
--   LINES TERMINATED BY '\n';


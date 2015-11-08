SELECT
    forge.typeID,
    invTypes.typeName,
    citadel.price citadelSell,
    citadel.volRemaining citadelUnits,
    forge.price forgeBuy,
    forge.volRemaining forgeUnits
FROM `marketOrders` forge 
INNER JOIN `marketOrders` citadel
    ON citadel.typeID = forge.typeID
    AND citadel.price < forge.price
INNER JOIN invTypes 
    ON forge.typeID = invTypes.typeID
WHERE forge.regionID = 10000002 AND forge.bid = 1
    AND citadel.regionID = 10000033 AND citadel.bid = 0
    AND forge.minVolume = 1
    AND ABS(TIMESTAMPDIFF(HOUR, forge.generationDate, citadel.generationDate)) < 24 
    AND forge.typeID = 34
ORDER BY forge.typeID ASC
LIMIT 10
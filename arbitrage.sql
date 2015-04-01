SELECT typeName, MIN(citadel.price) citadelSell, citadel.volRemaining, MAX(forge.price) forgeBuy, forge.volRemaining
FROM `marketOrdersMem` forge 
INNER JOIN `marketOrdersMem` citadel
ON citadel.typeID = forge.typeID
INNER JOIN invTypes 
ON forge.typeID=invTypes.typeID
WHERE forge.regionID = 10000002 AND forge.bid = 1
AND citadel.regionID = 10000033 AND citadel.bid = 0
AND citadel.price < forge.price
AND forge.minVolume = 1
GROUP BY forge.typeID, forge.regionID
ORDER BY ((MAX(forge.price) - MIN(citadel.price)) * LEAST(citadel.volRemaining, forge.volRemaining)) desc

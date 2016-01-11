SELECT prodType.typeID prodTypeID, prodType.typeName prodTypeName, prod.quantity prodQty, matType.typeName matTypeName, mat.quantity matQty, COALESCE(MIN(matOrder.price)*mat.quantity, 100000000000) matPrice, MIN(prodOrder.price)*prod.quantity prodPrice, COALESCE(attr.valueInt, attr.valueFloat) attrVal, SUM(history.quantity) AS volume
FROM industryActivityMaterials mat
INNER JOIN industryActivityProducts prod
    ON mat.typeID=prod.typeID
LEFT JOIN marketOrders matOrder
    ON mat.materialTypeID=matOrder.typeID
    AND matOrder.bid=0
    AND matOrder.regionID=10000002
INNER JOIN marketOrders prodOrder
    ON prod.productTypeID=prodOrder.typeID
    AND prodOrder.bid=0
    AND prodOrder.regionID=10000002
INNER JOIN invTypes matType
    ON mat.materialTypeID=matType.typeID
INNER JOIN invTypes prodType
    ON prod.productTypeID=prodType.typeID
LEFT JOIN dgmTypeAttributes attr
    ON prod.productTypeID=attr.typeID
    AND attr.attributeID=633
INNER JOIN industryActivity ia
    ON mat.typeID=ia.typeID AND ia.activityID=1
INNER JOIN marketHistory history
    ON prod.productTypeID=history.typeID AND history.regionID=10000002 AND date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
WHERE mat.activityID = 1
    AND (attr.valueInt = 0 OR attr.valueFloat = 0)
    AND prod.productTypeID=524
GROUP BY mat.typeID, mat.materialTypeID

SELECT prodTypeID typeID, prodTypeName, prodPrice, SUM(matPrice) matPrice, prodPrice-SUM(matPrice) profit, (prodPrice-SUM(matPrice))/time*60*60 iph, sum(history.volume) volume FROM (
    SELECT prodType.typeID prodTypeID, prodType.typeName prodTypeName, prod.quantity prodQty, matType.typeName matTypeName, mat.quantity matQty, MIN(matOrder.price) minPrice, COALESCE(MIN(matOrder.price)*mat.quantity, 100000000000) matPrice, MIN(prodOrder.price)*prod.quantity prodPrice, COALESCE(attr.valueInt, attr.valueFloat) attrVal, ia.time time
    FROM industryActivityMaterials mat
    INNER JOIN industryActivityProducts prod
        ON mat.typeID=prod.typeID
    LEFT JOIN marketOrders matOrder
        ON mat.materialTypeID=matOrder.typeID
        AND matOrder.bid=0
        AND matOrder.regionID=10000002
    INNER JOIN marketOrders prodOrder
        ON prod.productTypeID=prodOrder.typeID
        AND prodOrder.bid=0
        AND prodOrder.regionID=10000002
    INNER JOIN invTypes matType
        ON mat.materialTypeID=matType.typeID
    INNER JOIN invTypes prodType
        ON prod.productTypeID=prodType.typeID
    LEFT JOIN dgmTypeAttributes attr
        ON prod.productTypeID=attr.typeID
        AND attr.attributeID=633
    INNER JOIN industryActivity ia
        ON mat.typeID=ia.typeID AND ia.activityID=1
    WHERE mat.activityID = 1
        AND (attr.valueInt = 0 OR attr.valueFloat = 0)
    GROUP BY mat.typeID, mat.materialTypeID
) materialList
INNER JOIN (
    SELECT SUM(quantity)/30 AS volume, typeID
    FROM marketHistory
    WHERE date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
    AND regionID=10000002
    GROUP BY typeID
) history ON prodTypeID=history.typeID
where prodTypeID=524
GROUP BY typeID
ORDER BY iph DESC
LIMIT 100


1692 | metaGroupID
633 | metaLevel
422 | techLevel

var kue = require('kue');
var queue = kue.createQueue( { disableSearch: true } );

var mysql = require('mysql');
var connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '',
    database: 'eve'
});
connection.connect();
console.log("Connected");

process.once('SIGINT', function() {
    console.error("Shutting down gracefully...");
    queue.shutdown(function(err) {
        // queue.removeAllListeners();
        if (err)
            console.error(err);
        process.exit();
    }, 60000);
});

queue.on('job complete', function(id) {
    kue.Job.get(id, function(err, job) {
        if (job) {
            // console.log(job.type + " job completed in " + job.duration + "ms");
            job.remove();
        }
    });
});

queue.process('orders', 1, function(job, done) {
    // console.log("Processing job (" + (job.data.rowsets.length > 0 ? job.data.rowsets[0].rows.length : 0) + " orders)");

    // TODO: Support multiple rowsets
    if (job.data.rowsets.length != 1) {
        done("Messages with multiple rowsets are not yet supported. Rowset length was " + job.data.rowsets.length);
        return;
    }
    if (job.data.rowsets[0].rows.length < 1) {
        done(null, "No rows provided");
        return;
    }
    // TODO: Support columns in any order
    if (job.data.columns[0] != "price" ||
        job.data.columns[1] != "volRemaining" ||
        job.data.columns[2] != "range" ||
        job.data.columns[3] != "orderID" ||
        job.data.columns[4] != "volEntered" ||
        job.data.columns[5] != "minVolume" ||
        job.data.columns[6] != "bid" ||
        job.data.columns[7] != "issueDate" ||
        job.data.columns[8] != "duration" ||
        job.data.columns[9] != "stationID" ||
        job.data.columns[10] != "solarSystemID") {
        done("Unexpected column structure: " + job.data.columns);
        return;
    }
    
    connection.query('SELECT `generationDate` FROM `marketOrders` WHERE `typeID`=? AND `regionID`=? LIMIT 1', 
        [job.data.rowsets[0].typeID, job.data.rowsets[0].regionID], 
        function(err, rows, fields) {
            if (err) {
                console.error(err);
                done(err);
                return;
            }
            if (rows[0] && rows[0].generationDate && (rows[0].generationDate >= new Date(job.data.rowsets[0].generatedAt))) {
                done(null, "Incoming data was older than current data. Ours: " + rows[0].generationDate + " Theirs: " + job.data.rowsets[0].generatedAt);
                return;
            }

            var orderIDs = [];
            for (var i = 0; i < job.data.rowsets[0].rows.length; i++) {
                orderIDs.push(job.data.rowsets[0].rows[i][3]);
            }

            connection.query('DELETE FROM `marketOrders` WHERE `typeID`=? AND `regionID`=?' + (orderIDs.length > 0 ? ' AND `orderID` NOT IN (?)' : ''), 
                orderIDs.length > 0 ? [job.data.rowsets[0].typeID, job.data.rowsets[0].regionID, orderIDs] : [job.data.rowsets[0].typeID, job.data.rowsets[0].regionID], 
                function(err, result) {
                    if (err) {
                        console.error(err);
                        console.error("OrderID length was " + orderIDs.length);
                        done(err);
                        return;
                    }

                    console.log("Deleted rows: " + result.affectedRows);

                    for (var i = 0; i < job.data.rowsets[0].rows.length; i++) {
                        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].typeID);
                        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].regionID);
                        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].generatedAt);
                    }

                    if (job.data.rowsets[0].rows.length > 0)
                        connection.query('REPLACE INTO `marketOrders` (`price`,`volRemaining`,`range`,`orderID`,`volEntered`,`minVolume`,`bid`,`issueDate`,`duration`,`stationID`,`solarSystemID`,`typeID`,`regionID`,`generationDate`) VALUES ?', 
                            [job.data.rowsets[0].rows], 
                            function(err, result) {
                                if (err) {
                                    console.error(err);
                                    console.error("Rows length was " + job.data.rowsets[0].rows.length);
                                    done(err);
                                    return;
                                }

                                console.log("Updated rows: " + result.affectedRows);

                                done();
                            }
                        );
                    else
                        done();
                }
            );
        }
    );
});

queue.process('history', 1, function(job, done) {
    // console.log("Processing job (" + (job.data.rowsets.length > 0 ? job.data.rowsets[0].rows.length : 0) + " histories)");

    if (job.data.rowsets.length != 1) {
        done("Messages with multiple rowsets are not yet supported. Rowset length was " + job.data.rowsets.length);
        return;
    }
    if (job.data.rowsets[0].rows.length < 1) {
        done(null, "No rows provided");
        return;
    }

    for (var i = 0; i < job.data.rowsets[0].rows.length; i++) {
        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].typeID);
        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].regionID);
        job.data.rowsets[0].rows[i].push(job.data.rowsets[0].generatedAt);
    }

    connection.query('INSERT INTO `items_history` (`date`, `num_orders`, `quantity`, `price_low`, `price_high`, `price_average`, `type_id`, `region_id`, `created`) VALUES ? ON DUPLICATE KEY UPDATE `price_low`=VALUES(`price_low`), `price_high`=VALUES(`price_high`), `price_average`=VALUES(`price_average`), `quantity`=VALUES(`quantity`), `num_orders`=VALUES(`num_orders`)', 
        [job.data.rowsets[0].rows],
        function(err, rows, fields) {
            if (err) {
                console.error(err);
                done(err);
                return;
            }

            done();
        }
    );
});

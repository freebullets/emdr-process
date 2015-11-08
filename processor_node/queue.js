var zmq = require('zmq');
var sock = zmq.socket('sub');
var zlib = require('zlib');
var kue = require('kue');

var queue = kue.createQueue( { disableSearch: true } );  // Disables that pesky indexing overhead
var kue_app = kue.app.listen(3000);
kue.app.set('title', 'EMDR Job Monitor');

// Connect to the first publicly available relay.
sock.connect('tcp://relay-us-east-1.eve-emdr.com:8050');
// No filtering
sock.subscribe('');

process.once('SIGINT', function() {
    console.error("Shutting down gracefully...");
    sock.unsubscribe('');
    sock.close();
    kue_app.close();
    queue.shutdown(function(err) {
        queue.removeAllListeners();
        if (err)
            console.error(err);
        process.exit();
    }, 60000);
});

// Performs a task on each message received
sock.on('message', function(msg) {
    // Receive raw market JSON strings.
    zlib.inflate(msg, function(err, market_data) {
        // Un-serialize the JSON data.
        var market_json = JSON.parse(market_data);
        market_json.title = market_json.resultType;
        queue.create(market_json.resultType, market_json).save();
        console.log(market_json.resultType);
    });
});

// Removes obsolete completed jobs
queue.on('job complete', function(id) {
    kue.Job.get(id, function(err, job) {
        try {
            job.remove();
        } catch (err) {
            console.error("Could not remove job.");
        }
    });
});
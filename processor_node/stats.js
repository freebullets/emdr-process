// Subscribes to a given relay and logs the number of rowsets > 1
// Used to see if any clients were submitting multiple rowsets as the spec allows
// At the time of writing, there were none observed. However, I'm sure this has changed.

var zmq = require('zmq');
var sock = zmq.socket('sub');
var zlib = require('zlib');

// Connect to the first publicly available relay.
sock.connect('tcp://relay-us-east-1.eve-emdr.com:8050');
// Disable filtering
sock.subscribe('');

sock.on('message', function(msg) {
    // Receive raw market JSON strings.
    zlib.inflate(msg, function(err, market_data) {
        // Un-serialize the JSON data.
        var market_json = JSON.parse(market_data);
        if (market_json.rowsets.length > 1)
            console.log(market_json.rowsets.length);
    });
});
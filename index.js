var ws = require('ws');
var util = require('util');
var EventEmitter = require('events').EventEmitter;
var spawn = require('child_process').spawn;
var path = require('path');
var debug = require('debug');

var SkypeClass = function(options) {
  // -- Private variables
  var wss;
  var log = {pyOut: debug('skype:py:out'), pyErr: debug('skype:py:err'), main: debug('skype')};
  var wsport = 53295;
  var wshost = '127.0.0.1';
  var self = this;

  // -- Private functions
  var startServer = function(port, host) {
    wss = new ws.Server({port: port, host: host});
    wss.on('connection', serverListener);
  };
  var serverListener = function(client) {
    log.main('Client connected');
    client.on('message', function(message) {
      var obj;
      try {
        obj = JSON.parse(message);
      } catch(e) {
        log.main('Received unparsable string: %s', message);
        return;
      }
      if(obj.type == 'message') {
        self.emit('received message', obj.message)
      } else if(obj.type == 'onlinestatus') {
        self.emit('online status change', obj.user);
      } else if(obj.type == '') {

      } else {
        log.main('Received unknown type: %s', obj.type);
      }
    });
  };
  var startClient = function(port) {
    var script = path.join(__dirname, 'bin/skype.py');
    var python = spawn('python', [script, port]);
    python.stdout.on('data', function(data) {
      log.pyOut(data.toString());
    });
    python.stderr.on('data', function(data) {
      log.pyErr(data.toString());
    });
  };

  // -- Public functions
  self.init = function() {
    startServer(wsport, wshost);
    startClient(wsport);
  };

  // -- Execution
  return self;
};

util.inherits(SkypeClass, EventEmitter);
module.exports = SkypeClass;
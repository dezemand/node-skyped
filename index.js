var ws = require('ws');
var util = require('util');
var EventEmitter = require('events').EventEmitter;
var spawn = require('child_process').spawn;
var path = require('path');
var debug = require('debug');

JSON.sparse = function(json) {
  var obj;
  try {obj = JSON.parse(json);}
  catch(e) {return null;}
  return obj;
};

var SkypeClass = function(options) {
  // -- Private variables
  var wss, python, client;
  var self = this;
  var log = {pyOut: debug('skype:py:out'), pyErr: debug('skype:py:err'), main: debug('skype'), ws: debug('skype:ws')};
  var wsport = 53295;
  var wshost = '127.0.0.1';
  var ready = false;
  var cB = {getUser: {}, getChat: {}};

  // -- Private functions
  var startServer = function(port, host) {
    wss = new ws.Server({port: port, host: host});
    wss.on('connection', serverListener);
  };
  var serverListener = function(cl) {
    log.ws('client connection received');
    cl.send(JSON.stringify({action: 'init'}));
    cl.on('message', function(message) {
      var obj;
      if(!(obj = JSON.sparse(message))) return log.ws('unparsable message: %s', message);
      if(!obj.type) return log.ws('could not get type of message: %s', message);
      if(obj.type == 'init') {
        if(client) return log.ws('received valid init command, but wont override original client');
        client = cl;
        log.ws('valid init command received');
        if(!ready) {
          self.emit('ready');
          ready = true;
        }
      } else if(obj.type == 'message') {
        self.emit('received message', obj.message)
      } else if(obj.type == 'onlinestatus') {
        self.emit('online status change', obj.user);
      } else if(obj.type == 'userinfo') {
        if(cB.getUser[obj.user] && typeof(cB.getUser[obj.user]) == 'function') {
          cB.getUser[obj.user](null, obj.info);
          delete cB.getUser[obj.user];
        }
      } else if(obj.type == 'chatinfo') {
        if(cB.getChat[obj.handle] && typeof(cB.getChat[obj.handle]) == 'function') {
          cB.getChat[obj.handle](null, obj.info);
          delete cB.getUser[obj.user];
        }
      } else {
        log.ws('received unknown type: %s', obj.type);
      }
    });
    cl.on('close', function() {
      log.ws('client connection lost');
      if(cl == client) {
        client = null;
        log.ws('lost main client');
      }
    });
  };
  var startClient = function(port) {
    var script = path.join(__dirname, 'bin/skype.py');
    python = spawn('python', [script, port]);
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
  self.isConnected = function() {
    if(!wss) return false;
    if(!client) return false;
    return true;
  };
  self.getUser = function(username, callback) {
    if(!self.isConnected()) return log.main('getUser not allowed: not connected');
    if(callback && typeof(callback) == 'function') cB.getUser[username] = callback;
    client.send(JSON.stringify({action: 'userinfo', user: username}));
  };
  self.getChat = function(handle, callback) {
    if(!self.isConnected()) return log.main('getChat not allowed: not connected');
    if(callback && typeof(callback) == 'function') cB.getChat[handle] = callback;
    client.send(JSON.stringify({action: 'chatinfo', handle: handle}));
  };
  self.chatMessage = function(handle, body, callback) {
    if(!self.isConnected()) return log.main('chatMessage not allowed: not connected');
    if(!callback || typeof(callback) != 'function') callback = function() {};
    client.send(JSON.stringify({action: 'chatmessage', room: handle, body: body}));
  };
  self.userMessage = function(username, body, callback) {
    if(!self.isConnected()) return log.main('userMessage not allowed: not connected');
    if(!callback || typeof(callback) != 'function') callback = function() {};
    client.send(JSON.stringify({action: 'usermessage', user: username, body: body}));
  };

  // -- Execution
  if(options && typeof(options) == 'object') {
    if(options.port && typeof(options.port) == 'number') wsport = options.port;
    if(options.host && typeof(options.host) == 'string') wshost = options.host;
    if(options.start && options.start === true) self.init();
  }
  return self;
};

util.inherits(SkypeClass, EventEmitter);
module.exports = SkypeClass;
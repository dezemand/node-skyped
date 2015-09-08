var Skype = require('./index');

var skype = new Skype({start: true});

skype.on('received message', function(msg) {
  console.log('%s: %s', msg.from, msg.body);
});

skype.on('online status change', function(user) {
  console.log('%s changed his status to %s', user.username, user.onlineStatus);
});

skype.on('ready', function() {
  skype.chatMessage('', 'Hello!');
});
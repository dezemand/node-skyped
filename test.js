var Skype = require('./index');

var skype = new Skype();
skype.init();

skype.on('received message', function(msg) {
  console.log('%s: %s', msg.from, msg.body);
});

skype.on('online status change', function(user) {
  console.log('%s changed his status to %s', user.username, user.onlineStatus);
});

skype.on('ready', function() {
  skype.getUser('echo123', function(err, info) {
    console.log(info);
  });
  skype.getChat('#echo123/$000000000000', function(err, info) {
    console.log(info);
  });
});
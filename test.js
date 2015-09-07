/**
 * Created by mandj_000 on 2015-09-06.
 */

var Skype = require('./index');

var skype = new Skype();
skype.init();
skype.on('received message', function(msg) {
  console.log('%s: %s', msg.from, msg.body);
});
skype.on('online status change', function(user) {
  console.log('%s changed his status to %s', user.username, user.onlineStatus);
});
# skyped

## Notice

**Discontinued, skype no longer uses p2p chats. Also Skype is getting or already has their own kinds of bots.**

**skyped uses Skype4Py, which is no longer being updated and outdated. Skype4Py does not support cloud-based groupchats, so you wont receive *any* messages from those kind of chats. To make a P2P chat, use `/createmoderatedchat` in skype.**

## [Example](https://github.com/netraameht/node-skyped/blob/master/example.js)

```javascript
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
```

## Skype(options)

##### Options:
* `start` — Starts the bot after created.
* `host` — The host the websocket server is bound to.
* `port` — The port the websocket server (and client) is running on.

### Functions

#### Skype.init()

Starts both server and client on given host and port (default port is 53295 and host is localhost). This is not needed when you have `start` in options set to true.

#### Skype.isConnected()

Returns `true` if both the server and client are running, `false` otherwise.

#### Skype.getUser(username, callback)

Returns with details about the user.

* `username` — Username of the skype user (e.g. `echo123`)
* `callback(err, info)` — If success, `info` contains information about user.

#### Skype.getChat(handle, callback)

Returns with information about the chat room.

* `handle` — Conversation handle (e.g. `#echo123/$000aaaa00aa00a00`)
* `callback(err, info)` — Same as getUser, but will return with different info.

#### Skype.userMessage(username, body, callback)

Sends a message to a user using the user's username.

* `username` — Username of the skype user (e.g. `echo123`)
* `body` — Message
* `callback()` — Currently not called

#### Skype.chatMessage(handle, body, callback)

Sends a message to a user or chatroom using its conversation handle

* `handle` — Conversation handle (e.g. `#echo123/$000aaaa00aa00a00`)
* `body` — Message
* `callback()` — Currently not called

### Events

#### 'received message'

Is called when a message has been received/read/said. Returns with a message object.

#### 'user status change'

Is called when someone changes its online status. Returns with an user object.

#### 'ready'

Is called when Skype is ready and attached. This is only called once.

### Objects

#### Message object:

#### Chat object:

#### User object:

| Name | Description | 
| ---- | ----------- |
| Coming | Soon |

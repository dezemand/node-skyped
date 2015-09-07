import Skype4Py
import time
import json
import websocket
import sys

def FormatMessageObject(msg):
    obj = {
        'id': msg.Id,
        'body': msg.Body,
        'from': msg.FromHandle,
        'handle': msg.ChatName,
        'type': msg.Type,
        'time': int(msg.Timestamp),
        'status': msg.Status
    }
    return obj

def FormatUserObject(user):
    obj = {
        'about': user.About,
        'aliases': user.Aliases,
        'birthday': time.mktime(user.Birthday.timetuple()) if user.Birthday else None,
        'buddyStatus': user.BuddyStatus,
        'canLeaveVoicemail': user.CanLeaveVoicemail,
        'city': user.City,
        'country': user.Country,
        'countryCode': user.CountryCode,
        'displayName': user.DisplayName,
        'fullName': user.FullName,
        'username': user.Handle,
        'hasCallEquipment': user.HasCallEquipment,
        'homepage': user.Homepage,
        'isAuthorized': user.IsAuthorized,
        'isBlocked': user.IsBlocked,
        'isCallForwardActive': user.IsCallForwardActive,
        'isSkypeOutContact': user.IsSkypeOutContact,
        'isVideoCapable': user.IsVideoCapable,
        'isVoicemailCapable': user.IsVoicemailCapable,
        'language': user.Language,
        'languageCode': user.LanguageCode,
        'lastOnline': user.LastOnline,
        'moodText': user.MoodText,
        'numberOfAuthBuddies': user.NumberOfAuthBuddies,
        'onlineStatus': user.OnlineStatus,
        'phoneHome': user.PhoneHome,
        'phoneMobile': user.PhoneMobile,
        'phoneOffice': user.PhoneOffice,
        'province': user.Province,
        'receivedAuthRequest': user.ReceivedAuthRequest,
        'richMoodText': user.RichMoodText,
        'sex': user.Sex,
        'speedDial': user.SpeedDial,
        'timezone': user.Timezone
    }
    return obj

def FormatChatObject(chat):
    obj = {
         'activityTimestamp': chat.ActivityTimestamp,
         'adder': user_handle_mapper(chat.Adder),
         'applicants': map(user_handle_mapper, chat.Applicants),
         'blob': chat.Blob,
         'bookmarked': chat.Bookmarked,
         'description': chat.Description,
         'dialogPartner': chat.DialogPartner,
         'friendlyName': chat.FriendlyName,
         'guideLines': chat.GuideLines,
         'members': map(user_handle_mapper, chat.Members),
         'myRole': chat.MyRole,
         'myStatus': chat.MyStatus,
         'name': chat.Name,
         'passwordHint': chat.PasswordHint,
         'posters': map(user_handle_mapper, chat.Posters),
         'status': chat.Status,
         'timestamp': chat.Timestamp,
         'topic': chat.Topic,
         'type': chat.Type
    }
    return obj

def OnMessageStatus(msg, status):
    msgf = FormatMessageObject(msg)
    obj = {
        'type': 'message',
        'message': msgf
    }
    ws.send(json.dumps(obj))

def OnOnlineStatus(user, status):
    userf = FormatUserObject(user)
    obj = {
        'type': 'onlinestatus',
        'user': userf
    }
    ws.send(json.dumps(obj))

def wsOpen(ws):
    print 'Websocket connected, attaching to skype...'
    skype.OnMessageStatus = OnMessageStatus
    skype.OnOnlineStatus = OnOnlineStatus
    skype.Attach()

def wsMessage(ws, message):
    obj = json.loads(message)
    if obj['action'] == 'exit':
        sys.exit()
    elif obj['action'] == 'send':
        chat = skype.Chat(obj['room'])
        chat.SendMessage(obj['message'])
    elif obj['action'] == '':
        ws.

def wsError(ws, error):
    print 'Websocket error: ' + str(error)

def wsClose(ws):
    print 'Websocket disconnected'

def main(argv):
    if len(argv) < 2:
        print 'Usage: ' + argv[0] + ' <port> [host]'
        return
    if len(argv) > 2:
        host = argv[2]
    else:
        host = '127.0.0.1'
    port = argv[1]
    print 'Connecting to websocket server on ' + host + ':' + port
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp('ws://' + host + ':' + port + '/', on_message = wsMessage, on_error = wsError, on_close = wsClose)
    global ws
    ws.on_open = wsOpen
    ws.run_forever()

if __name__ == "__main__":
    skype = Skype4Py.Skype()
    main(sys.argv)
import Skype4Py
import time
import json
import pprint
import websocket

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
        'handle': user.Handle,
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

def OnMessageStatus(msg, status):
    obj = FormatMessageObject(msg)
    print json.dumps(obj)

def OnOnlineStatus(user, status):
    obj = FormatUserObject(user)
    print json.dumps(obj)

def OnCommand(command):
    print command

def wsOpen(ws):
    print 'Websocket connected'
    print 'Connecting to Skype'
    skype = Skype4Py.Skype()
    skype.OnMessageStatus = OnMessageStatus
    skype.OnOnlineStatus = OnOnlineStatus
    skype.OnCommand = OnCommand
    skype.Attach()

def wsMessage(ws, message):
    print message

def wsError(ws, error):
    print error

def wsClose(ws):
    print 'Websocket disconnected'

if __name__ == "__main__":
    print 'Connecting to websocket server'
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://echo.websocket.org/", on_message = wsMessage, on_error = wsError, on_close = wsClose)
    ws.on_open = wsOpen
    ws.run_forever()

# Author: Tao Zheng
# Email:  ztao10001@gmail.com
# Date:   2020-08-05
# Ref:
# https://towardsdatascience.com/accessing-google-calendar-events-data-using-python-e915599d3ae2
# https://developers.google.com/calendar/create-events

from __future__ import print_function
import datetime
import datefinder
import pickle
import os.path
import pprint as pp
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def authenticate_google_cal():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    Create a recurring events based on my needs.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

    # result = service.calendarList().list().execute()
    # print(result)
    # 'id': '9cg69pl30qmr2b4g9ov0hcinmk@group.calendar.google.com',

    # Call the Calendar API
    # now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    # print('Getting the upcoming 10 events')
    # events_result = service.events().list(calendarId='primary', timeMin=now,
    #                                     maxResults=10, singleEvents=True,
    #                                     orderBy='startTime').execute()
    # events = events_result.get('items', [])

    # if not events:
    #     print('No upcoming events found.')
    # for event in events:
    #     start = event['start'].get('dateTime', event['start'].get('date'))
    #     print(start, event['summary'])

def create_event(start_time_str, summary, duration=1, attendees=None, description=None, location=None):

    matches = list(datefinder.find_dates(start_time_str))
    if len(matches):
        start_time = matches[0]
        end_time = start_time + datetime.timedelta(hours=duration)
                
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Detroit',
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'America/Detroit',
        },
        'reminders': {
            'useDefault': True,
            # 'overrides': [
            #     # {'method': 'email', 'minutes': 24 * 60},
            #     {'method': 'popup', 'minutes': 30},
            # ],
        },
    }

    # print(type(start_time))
    # print(start_time)
    # pp.pprint('''*** %r event added: 
    # With: %s
    # Start: %s
    # End:   %s''' % (summary.encode('utf-8'),
    #     attendees,start_time, end_time))
        
    return service.events().insert(calendarId='9cg69pl30qmr2b4g9ov0hcinmk@group.calendar.google.com', body=event).execute()

# # Refer to the Python quickstart on how to setup the environment:
# # https://developers.google.com/calendar/quickstart/python
# # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
# # stored credentials.

# event = {
#   'summary': 'Google I/O 2015',
#   'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2015-05-28T09:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'end': {
#     'dateTime': '2015-05-28T17:00:00-07:00',
#     'timeZone': 'America/Los_Angeles',
#   },
#   'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }

# event = service.events().insert(calendarId='primary', body=event).execute()
# print 'Event created: %s' % (event.get('htmlLink'))

creds = authenticate_google_cal()
service = build('calendar', 'v3', credentials=creds)

Start_Time = "2020-08-11 09:00:00"
Exp_Days = [0, 1, 3, 7, 14, 21, 28, 35]
User_Name = "Yunki"
Exp = "One-month MN patch in [PBST + 25% Ethanol]"

for Exp_Day in Exp_Days:
    
    matches = list(datefinder.find_dates(Start_Time))
    if len(matches):
        Exp_Time = str(matches[0] + datetime.timedelta(days=Exp_Day))

    detail = User_Name + "'s " + Exp + ": " + "Day" + str(Exp_Day) + ", " + "ExpID: " + User_Name[0] + Start_Time[0:10]

    time_slot = 1

    create_event(Exp_Time, detail, time_slot)
    print("created " + detail)

print("Success!")
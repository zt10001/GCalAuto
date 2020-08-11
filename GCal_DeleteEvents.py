# Author: Tao Zheng
# Email:  ztao10001@gmail.com
# Date:   2020-08-05
# Ref:
# https://towardsdatascience.com/accessing-google-calendar-events-data-using-python-e915599d3ae2
# https://developers.google.com/calendar/v3/reference/events/delete

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


def get_event_id_list(q_text):
    id_list = []
    
    events_result = service.events().list(calendarId='9cg69pl30qmr2b4g9ov0hcinmk@group.calendar.google.com',
                                          q=q_text).execute()
    events = events_result.get('items', [])

    if not events:
        print('No events found.')
    for event in events:
        # start = event['start'].get('dateTime', event['start'].get('date'))
        id_list.append(event['id'])
    
    return id_list

def delete_event(id_list):
    for id in id_list:
        service.events().delete(calendarId='9cg69pl30qmr2b4g9ov0hcinmk@group.calendar.google.com',
                                            eventId=id).execute()
        print("deleting " + id)

creds = authenticate_google_cal()
service = build('calendar', 'v3', credentials=creds)

ExpID = "J2020-08-04"

id_list = get_event_id_list(ExpID)

delete_event(id_list)

print("Success!")
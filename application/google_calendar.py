from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
CLIENT_SECRET_FILE = 'config/client_secret.json'
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.
    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.
    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir, 'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def get_upcoming_events(calendar_id='primary', max_results=10):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)

    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print('Getting the upcoming {} events'.format(max_results))
    events_result = service.events().list(
        calendarId=calendar_id, timeMin=now, maxResults=max_results, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        return []
    else:
        return events


def events_from_now(events):
    """make a new list with events available from now"""

    now = datetime.datetime.now()
    available_events = []

    for event in events:

        y, mo, d, h, mi, s = extract_datetime(event['start'].get('dateTime'))
        date_text = y + '/' + mo + '/' + d + " " + h + ':' + mi + ':' + s
        start_time = datetime.datetime.strptime(date_text, '%Y/%m/%d %H:%M:%S')

        if start_time > now:
            available_events.append(event)

    return available_events


def events_today(events):
    """make a new list with events available only today"""

    today = datetime.date.today()
    available_events = []

    for event in events:

        y, mo, d, h, mi, s= extract_datetime(event['start'].get('dateTime'))
        date_text = y + '/' + mo + '/' + d + " " + h + ':' + mi + ':' + s
        date = datetime.datetime.strptime(date_text, '%Y/%m/%d %H:%M:%S').date()

        if date == today:
            available_events.append(event)

    return available_events


def extract_datetime(datetime_text):
    ymd, time = datetime_text.split('T')
    year, month, date = ymd.split('-')
    hms, _ = time.split('+')
    hour, minute, second = hms.split(':')
    return year, month, date, hour, minute, second


def events2text(calendar_id='primary', max_results=10):
    events = get_upcoming_events(calendar_id, max_results)
    text = ''
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        sy, smo, sd, sh, smi, ss = extract_datetime(start)
        ey, emo, ed, eh, emi, es = extract_datetime(end)
        text += '{}/{} {}:{}〜{}:{} {}\n'.format(smo, sd, sh, smi, eh, emi, summary)

    return text


def events2text_custom(events):

    text = ''
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        summary = event['summary']
        sy, smo, sd, sh, smi, ss = extract_datetime(start)
        ey, emo, ed, eh, emi, es = extract_datetime(end)
        text += '{}/{} {}:{}〜{}:{} {}\n'.format(smo, sd, sh, smi, eh, emi, summary)

    return text



if __name__ == '__main__':
    import pprint

    calendar_ids = {'swordart': 'g9f9k8e0tal8nohjb2bt9eimvo@group.calendar.google.com',
                    'marianne': 'b5hemoec1ol2uo5omk1pvmqbvc@group.calendar.google.com',
                    'honnoji': 'k9k5kfnrehfomillqffi1kpe7g@group.calendar.google.com'}

    swordart_events = get_upcoming_events(calendar_id=calendar_ids['swordart'], max_results=100)
    marianne_events = get_upcoming_events(calendar_id=calendar_ids['marianne'], max_results=100)
    honnoji_events = get_upcoming_events(calendar_id=calendar_ids['honnoji'], max_results=100)

    #for key in calendar_ids:
    #pprint.pprint(events_today(get_upcoming_events(calendar_id=calendar_ids['honnoji'])))
    pprint.pprint(events_from_now(get_upcoming_events(calendar_id=calendar_ids['honnoji'])))
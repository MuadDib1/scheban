# -*- coding: utf-8 -*-
import sys
from slackbot.bot import respond_to
sys.path.append('..')
from google_calendar import events2text


@respond_to('今後の予定を教えて')
def respond_schedule(message):
    calendar_id = ''
    reply_message = events2text(calendar_id=calendar_id)
    message.reply(reply_message)

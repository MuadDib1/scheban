# -*- coding: utf-8 -*-
import sys
from slackbot.bot import respond_to
sys.path.append('..')
from application.google_calendar import events_today, events_from_now, get_upcoming_events, events2text_custom


calendar_ids = {'swordart': 'g9f9k8e0tal8nohjb2bt9eimvo@group.calendar.google.com',
                    'marianne': 'b5hemoec1ol2uo5omk1pvmqbvc@group.calendar.google.com',
                    'honnoji': 'k9k5kfnrehfomillqffi1kpe7g@group.calendar.google.com'}

@respond_to('今日の映畫を教えて')
def respond_schedule_today(message):
    #calendar_id = 'k9k5kfnrehfomillqffi1kpe7g@group.calendar.google.com'
    #reply_message = events2text(calendar_id=calendar_id)
    #swordart_events = get_upcoming_events(calendar_id=calendar_ids['swordart'], max_results=100)
    #marianne_events = get_upcoming_events(calendar_id=calendar_ids['marianne'], max_results=100)
    #honnoji_events = get_upcoming_events(calendar_id=calendar_ids['honnoji'], max_results=100)

    for key in calendar_ids:
        reply_message = events2text_custom(
            events_from_now(events_today(get_upcoming_events(calendar_id=calendar_ids[key]))))
        message.reply(reply_message)


@respond_to('ソードアートのスケジュールを見せて')
def respond_schedule_swordart(message):
    reply_message = events2text_custom(
        events_from_now(get_upcoming_events(calendar_id=calendar_ids['swordart'])))
    message.reply(reply_message)


@respond_to('マリアンヌのスケジュールを見せて')
def respond_schedule_swordart(message):
    reply_message = events2text_custom(
        events_from_now(get_upcoming_events(calendar_id=calendar_ids['marianne'])))
    message.reply(reply_message)


@respond_to('本能寺ホテルのスケジュールを見せて')
def respond_schedule_swordart(message):
    reply_message = events2text_custom(
        events_from_now(get_upcoming_events(calendar_id=calendar_ids['honnoji'])))
    message.reply(reply_message)

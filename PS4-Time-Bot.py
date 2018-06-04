#!/usr/bin/env
# -*- coding: utf-8 -*-

"""
"""

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import sys
import csv
import dateutil.parser
import pytz
from datetime import datetime, timedelta, timezone
from icalendar import Calendar, Event
from pprint import pprint
import operator
from dateutil.tz import tzutc

"""------------------Vars------------------"""
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

filePath = "Path\to\file"
BotID = "Telegram Token"
formatDate = "%Y%m%dT%H%M%SZ"

# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
"""------------------Commands------------------"""


def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(bot, update):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


def GetAllTimes(bot, update):
    ComposeAndSendMsg(update, "all", "m")


def GetLastMonthTimes(bot, update):
    ComposeAndSendMsg(update, "month", "m")


def GetLastWeekTimes(bot, update):
    ComposeAndSendMsg(update, "week", "m")


def GetTodayTimes(bot, update):
    ComposeAndSendMsg(update, "today", "m")


def GetAllTimesHours(bot, update):
    ComposeAndSendMsg(update, "all", "h")


def GetLastMonthTimesHours(bot, update):
    ComposeAndSendMsg(update, "month", "h")


def GetLastWeekTimesHours(bot, update):
    ComposeAndSendMsg(update, "week", "h")


def GetTodayTimesHours(bot, update):
    ComposeAndSendMsg(update, "today", "h")


"""------------------Functions------------------"""


def ComposeAndSendMsg(update, timeframe, time_format):
    msg_header = ""
    dates = GetTimes(timeframe)
    statistics = MakeStatistics(dates, time_format)
    timespanStartDate = GetFirstDate(dates).strftime("%d-%m-%Y")
    timespanEndDate = GetLastDate(dates).strftime("%d-%m-%Y ")
    msg_header_timespan = "\n" + "From " + timespanStartDate + " to " + timespanEndDate + "\n"

    if (timeframe == "week"):
        msg_header = "Games played last week:" + msg_header_timespan
    elif (timeframe == "all"):
        msg_header = "Games played:" + msg_header_timespan
    elif (timeframe == "today"):
        msg_header = "Games played today:" + msg_header_timespan
    elif (timeframe == "month"):
        msg_header = "Games played last month:" + msg_header_timespan
    else:
        msg_header = "Games played:"

    SendMsg(update, statistics, msg_header, time_format)



def GetFirstDate(dates):
    beginningElement = dates[0]
    startDate = beginningElement['date']

    return startDate


def GetLastDate(dates):
    endingElement = dates[len(dates) - 1]
    endDate = endingElement['date']

    return endDate


def SendMsg(update, statistics, msg_header, time_format):
    statisticsCSV = sortAndFormatStatistics(statistics, msg_header, time_format)
    update.message.reply_text(statisticsCSV)


def GetTimes(timeframe):
    dates = getDates(filePath)
    logging.info("Found %s dates", len(dates))
    print("Found %s dates", len(dates))

    if (timeframe == "week"):
        return GetTimesInTimeframe(dates, 7)
    elif (timeframe == "month"):
        return GetTimesInTimeframe(dates, 30)
    elif (timeframe == "today"):
        return GetTimesInTimeframe(dates, 1)
    elif (timeframe == "all"):
        return dates
    else:
        return dates


def GetTimesInTimeframe(dates, timeframe_in_days):
    dayLastWeekUTC = datetime.now(timezone.utc) - timedelta(days=timeframe_in_days)
    dayLastWeek = dayLastWeekUTC.replace(tzinfo=tzutc())
    datesInTimeframe = []

    for date in dates:
        for key in date:
            value = date[key]
            if isinstance(value, datetime):
                if value > dayLastWeek:
                    datesInTimeframe.append(date)

    return datesInTimeframe


def MakeStatistics(dates, time_format):
    cal = MakeTimes(dates)
    statistics = getStatistics(cal, time_format)
    return statistics


def MakeTimes(dates):
    """Send a message when the command /GetTimes is issued."""
    """update.message.reply_text('Times!')"""

    i = 0
    timeSpanBeginDate = ""
    calendar_event = None
    icalString = []

    cal = Calendar()
    cal['summary'] = 'Playstation 4 Playtime'

    while i < len(dates):

        if (i == 0):
            print("First element")
            timeSpanBeginDate = dates[i]
        elif (isBeginOfTimespan(dates[i - 1], dates[i])):
            print("Timespan Begin ")
            calendar_event = None
            timeSpanBeginDate = dates[i]
        elif (i + 1 == len(dates)):
            print("Last Element")
            calendar_event = getIcalDate(timeSpanBeginDate, dates[i])
        elif (isBeginOfTimespan(dates[i], dates[i + 1])):
            print("Timespan End ")
            calendar_event = getIcalDate(timeSpanBeginDate, dates[i])

        if calendar_event is not None and timeSpanBeginDate['game'] != "null" and timeSpanBeginDate[
            'game'] != "PowerOff":
            print("Adding event", calendar_event)
            cal.add_component(calendar_event)

        i = i + 1

    return cal


def getDates(alertsFilename):
    dates = []
    with open(alertsFilename) as csvfile:
        alertsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in alertsreader:
            date = {}
            date['date'] = dateutil.parser.parse(row[0])
            date['game'] = row[1]
            date['id'] = row[2]
            dates.append(date)

    return dates


def getStatistics(dates, time_format):
    divideBy = 60
    if (time_format == "m"):
        divideBy = divideBy
    elif (time_format == "h"):
        divideBy = divideBy * 60

    statistics = {}
    for date in dates.walk():
        if (date.name == "VEVENT"):
            s1 = date['DTSTART']
            s2 = date['DTEND']
            tdelta = datetime.strptime(s2, formatDate) - datetime.strptime(s1, formatDate)
            name = date['DESCRIPTION']
            time = tdelta.seconds / divideBy
            thisDuration = round(time, 2)

            if date['DESCRIPTION'] in statistics:
                totalDuration = thisDuration + statistics[date['DESCRIPTION']]
            else:
                totalDuration = thisDuration

            statistics[date['DESCRIPTION']] = totalDuration

    return statistics


def sortAndFormatStatistics(statistics, msg_header_text, time_format):
    TimeFormat = ""
    if (time_format == "m"):
        TimeFormat = "min"
    elif (time_format == "h"):
        TimeFormat = "h"

    outString = msg_header_text + "\n"

    sorted_statistic = sorted(statistics, key=statistics.get, reverse=True)

    for stat in sorted_statistic:
        outString = outString + stat + ", " + str(statistics[stat]) + TimeFormat + "\n"

    return outString


def isBeginOfTimespan(currentElement, elementBefore):
    if (currentElement['id'] != elementBefore['id']):
        return True
    else:
        return False


def isEndOfTimespan(currentElement, nextElement):
    pass


def getIcalDate(beginningElement, endingElement):
    calendar_event = Event()
    game = beginningElement['game']
    calendar_event.add('summary', game)

    startDate = beginningElement['date']
    endDate = endingElement['date']

    calendar_event['DTSTART'] = startDate.strftime(formatDate)
    calendar_event['DTEND'] = endDate.strftime(formatDate)

    calendar_event.add('description', game)
    if (game is not None and game is not ""):
        return calendar_event
    else:
        return None


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(BotID)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    """1. Wort in Chat, 2. Funktion die gerufen wird"""
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    """----times----"""
    dp.add_handler(CommandHandler("times_all", GetAllTimes))
    dp.add_handler(CommandHandler("times_last_month", GetLastMonthTimes))
    dp.add_handler(CommandHandler("times_last_week", GetLastWeekTimes))
    dp.add_handler(CommandHandler("times_today", GetTodayTimes))

    """----timesH----"""
    dp.add_handler(CommandHandler("times_all_h", GetAllTimesHours))
    dp.add_handler(CommandHandler("times_last_month_h", GetLastMonthTimesHours))
    dp.add_handler(CommandHandler("times_last_week_h", GetLastWeekTimesHours))
    dp.add_handler(CommandHandler("times_today_h", GetTodayTimesHours))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
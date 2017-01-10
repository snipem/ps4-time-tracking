#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import sys
import csv
import dateutil.parser
import pytz
from datetime import datetime
from icalendar import Calendar, Event
from pprint import pprint

import logging
logging.basicConfig(level=logging.DEBUG)
formatDate = "%Y%m%dT%H%M%SZ"

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

def getStatistics(dates):
    statistics = {}
    for date in dates.walk():
        if (date.name == "VEVENT"):
            s1 = date['DTSTART']
            s2 = date['DTEND']
            tdelta = datetime.strptime(s2, formatDate) - datetime.strptime(s1, formatDate)
            name = date['DESCRIPTION']
            thisDuration = tdelta.seconds/60

            if (statistics.has_key(date['DESCRIPTION'])):
                totalDuration = thisDuration + statistics[date['DESCRIPTION']]
            else:
                totalDuration = thisDuration

            statistics[date['DESCRIPTION']] = totalDuration

    return statistics

def sortAndFormatStatistics(statistics):
    outString = ""

    for statistic in statistics:
        outString = outString + statistic + "," + str(statistics[statistic]) + "\n"

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


if __name__ == '__main__':

    if (len(sys.argv) != 3):
        print "usage: parseTimeSpans.py logfile.log out.ics"
        sys.exit(-1)

    dates = getDates(sys.argv[1])
    logging.info("Found %s dates", len(dates))

    i = 0
    timeSpanBeginDate = ""
    calendar_event = None
    icalString = []

    cal = Calendar()
    cal['summary'] = 'Playstation 4 Playtime'

    while i < len(dates):

        if (i == 0):
            print ("First element")
            timeSpanBeginDate = dates[i]
        elif (isBeginOfTimespan(dates[i-1],dates[i])):
            print ("Timespan Begin ")
            calendar_event = None
            timeSpanBeginDate = dates[i]
        elif (i+1 == len(dates)):
            print ("Last Element")
            calendar_event = getIcalDate(timeSpanBeginDate, dates[i])
        elif (isBeginOfTimespan(dates[i],dates[i+1])):
            print ("Timespan End ")
            calendar_event = getIcalDate(timeSpanBeginDate, dates[i])

        if calendar_event is not None and timeSpanBeginDate['game'] != "null" and timeSpanBeginDate['game'] != "PowerOff":
            print("Adding event",calendar_event)
            cal.add_component(calendar_event)

        i=i+1

    statistics = getStatistics(cal)
    statisticsCSV = sortAndFormatStatistics(statistics)

    f = open(sys.argv[2], 'w')
    f.write(cal.to_ical())

    f = open("statistics.csv", 'w')
    f.write(statisticsCSV.encode('UTF-8'))

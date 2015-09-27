import sys
import csv
import dateutil.parser
import pytz
from datetime import datetime
from icalendar import Calendar, Event
from pprint import pprint

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

dates = getDates(sys.argv[1])

def isBeginOfTimespan(currentElement, elementBefore):
    if (currentElement['id'] != elementBefore['id']):
        return True
    else:
        return False

def isEndOfTimespan(currentElement, nextElement):
    pass

def getIcalDate(beginningElement, endingElement):

    event = Event()
    game = beginningElement['game']
    event.add('summary', game)

    startDate = beginningElement['date']
    endDate = endingElement['date']

    formatDate = "%Y%m%dT%H%M%SZ"

    event['DTSTART'] = startDate.strftime(formatDate)
    event['DTEND'] = endDate.strftime(formatDate)

    event.add('description', game)
    if (game is not None and game is not ""):
        return event
    else:
        return None

i = 0
timeSpanBeginDate = ""
event = None
icalString = []

cal = Calendar()
cal['summary'] = 'Playstation 4 Playtime'

while i < len(dates):

    if (i == 0):
        print ("First element")
        timeSpanBeginDate = dates[i]
    elif (isBeginOfTimespan(dates[i-1],dates[i])):
        print ("Timespan Begin ")
        event = None
        timeSpanBeginDate = dates[i]
    elif (i+1 == len(dates)):
        print ("Last Element")
        event = getIcalDate(timeSpanBeginDate, dates[i])
    elif (isBeginOfTimespan(dates[i],dates[i+1])):
        print ("Timespan End ")
        event = getIcalDate(timeSpanBeginDate, dates[i])

    if event != None and event != 'null' and timeSpanBeginDate['game'] != "null" and timeSpanBeginDate['game'] != "PowerOff":
        print("Adding event",event)
        cal.add_component(event)

    i=i+1

f = open(sys.argv[2], 'w')
f.write(cal.to_ical())

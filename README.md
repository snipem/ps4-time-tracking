# ps4-time-tracking

This program helps you keep track of your PS4 gaming habits. It will create an [iCalendar](https://en.wikipedia.org/wiki/ICalendar) file which contains timespans from the time you were playing.

## Requirements
The tools Python, `ps4-wake` and `jq` are needed for this process.
`ps4-wake` will be built by running `build.sh`. `jq` for JSON parsing and Python can be obtained by your distribution.

## Usage
Run `ps4watch.sh` in very short frequency to track what game your PS4 is
running at the time. After an amount of time the log file will fill with dates:

``` csv
2016-08-12T14:55+0000,null,null
2016-08-12T15:00+0000,null,null
2016-08-12T15:05+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:10+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:15+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:20+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:25+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:30+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:35+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:40+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:45+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:50+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T15:55+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T16:00+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T16:05+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T16:10+0000,"Pro Evolution Soccer 2016","CUSA02640"
2016-08-12T16:15+0000,"Destiny","CUSA00219"
2016-08-12T16:20+0000,"Destiny","CUSA00219"
2016-08-12T16:25+0000,"Destiny","CUSA00219"
2016-08-12T16:30+0000,"Destiny","CUSA00219"
```

You can generate calendar entries in ics format by running `parseTimeSpans.py ps4watch.log calendar.ics`.

Run `ps4ical.sh` to calculate time-spans and to generate an `ics` file out of it. Adapt it to your needs. Currently it contains a statement for FTP uploading to my server.

If you're subscribing to this calendar, you will get a nice output:

![Output in Calendar](example.png?raw=true "Output in Calendar")

Additionally a file called `statistics.csv` is generated which summarizes
all minutes that you played one particular game.

## Example crontab

The following crontab setting will run `ps4watch.sh` every 5 minutes between 10pm till 2am and every half hour between 3 am and 9 pm.

``` crontab
*/5 10-23 * * * ps4watch.sh
*/5 0-2 * * * ps4watch.sh
*/30 3-9 * * * ps4watch.sh
```

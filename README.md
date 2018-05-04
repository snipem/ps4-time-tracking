# ps4-time-tracking

This program helps you keep track of your PS4 gaming habits. It will create an [iCalendar](https://en.wikipedia.org/wiki/ICalendar) file which contains timespans from the time you were playing.

## Requirements
The tools Python, `ps4-wake` and `jq` are needed for this process.
`ps4-wake` will be built by running `build.sh`. `jq` for JSON parsing and Python can be obtained by your distribution.
If you want to use the Telegram Bot you need to install [this Bot Framework](https://github.com/python-telegram-bot/python-telegram-bot) first.

### Prerequisites
Install build-essentials (for make), pip, jq from your distribution

1. Install Prerequisites
2. Run `build.sh`
3. Copy the resulting `ps4-wake` to your bin path i.e. `/usr/bin`
4.  Install the Python requirements with `pip install -r
requirements.txt`.

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

`makeScore.sh` is also a utilty custom made for my needs, which will generate a top 10 list of my top games and will notify me whenever a different game enters or moves up the top 10.

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

## Bot Usage
Create new Telegram Bot via Telegrams own BotFather and insert your newly created Api Token in PS4-Time-Bot.py.
In addition to your Api Token you need to specify the path to your ps4watch.log file.
Thats it, now you can start PS4-Time-Bot.py with python3 and use your Telegram Bot.

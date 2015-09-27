# ps4-time-tracking

This program helps you keep track of your PS4 gaming habits. It will create an iCalendar file which contains timespans from the time you were playing.

## Usage

Run `ps4watch.sh` in very short frequency to track what game your PS4 is running at the time. The tools `ps4-wake` and `jq` are needed for this process.
`ps4-wake` will be built be running `build.sh`. `jq` can be obtained by your distribution.

Run `ps4ical.sh` to calculate timespans and to generate an `ics` file out of it. Adapt it to your needs. Currently it contains a statement for FTP uploading to my server.

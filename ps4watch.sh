#!/bin/sh
json=`ps4wake -P -B -j`;
timestamp=`echo $json | jq .timestamp`
dateCheck=`python -c "from datetime import datetime; print (datetime.now().isoformat())"`
echo "$dateCheck,$(echo $json | jq .running_app_name),$(echo $json | jq .running_app_titleid)" >> ~/log/ps4watch.log

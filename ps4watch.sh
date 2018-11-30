#!/bin/sh
dir="$HOME/log"
[ -d $dir ] || mkdir -p "$dir"
./ps4watch.py >> $dir/ps4watch.log


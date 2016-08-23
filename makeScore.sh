#!/bin/bash
cat statistics.csv | sort --field-separator="," -n --key=2 --reverse > statistics_sorted.csv

cat -n statistics_sorted.csv | awk -F"," '{print $1}' > statistics_sorted_score.csv
cat -n statistics_sorted_old.csv | awk -F"," '{print $1}' > statistics_sorted_score_old.csv

diff <(head -n 10 statistics_sorted_score_old.csv) <(head -n 10 statistics_sorted_score.csv) | pushover_pipe

cp statistics_sorted.csv statistics_sorted_old.csv

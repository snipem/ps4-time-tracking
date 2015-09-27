python2 parseTimeSpans.py ~/log/ps4watch.log ps4_play.ics

checksum_new=`md5sum ps4_play.ics | awk '{print $1}'`
if [ "$checksum_old" = "$checksum_new" ]; then 
	exit
else
	echo $checksum_old
	echo $checksum_new    
    	~/bin/ftpcp ps4_play.ics wolke/ps4_play.ics
fi;

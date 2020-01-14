#!/bin/bash
#
#

DIR=`dirname $(readlink -f $0)`

. /home/www/cgi-bin/include/functions
. league.dat
cgiVars

# what is the timestamp of today @ 0:00
dayNow=$(date -d"0:00" +%s)
if [ ${CGI_gid} != "" ] ; then
  IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT PF PA < <(grep "${CGI_gid}" ${SCHEDULE})
  echo "$GAME_ID $GAME_TIMESTAMP $GAME_DAY $GAME_START" >> /tmp/whoscoming-divs.input
else
  # look for the first entry in the schedule that is greater than 'dayNow'
  origIFS=$IFS
  IFS='~'
  while read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT PF PA; do
    if [ $GAME_TIMESTAMP -ge $dayNow ] ; then
      echo "GAME_ID: ${GAME_ID}" >> /tmp/whoscoming.log
      break;
    fi;
         # sort by GAME_TIMESTAMP
  done < <(sort -t~ -k2,2 -n ${SCHEDULE})
  IFS=$ofigIFS
fi


. ${DIR}/admin/functions
. ${DIR}/admin/attendance.func

htmlHeader
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ATTENDANCE|active|" template-header.html

printBootAttendancePage public
cat template-footer.html

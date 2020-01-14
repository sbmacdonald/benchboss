#!/bin/bash
#
#
. league.dat
. /home/www/cgi-bin/include/functions
cgiVars

# what is the timestamp of today @ 0:00
dayNow=$(date -d"0:00" +%s)

if [ "${CGI_gameId}" != "" ] ; then
  IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT PF PA < <(grep "${CGI_gameId}" ${SCHEDULE})
  #echo "$GAME_ID $GAME_TIMESTAMP $GAME_DAY $GAME_START" >> /tmp/whoscoming-divs.input
else
  # look for the first entry in the schedule that is greater than 'dayNow'
  IFS='~'
  while read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT PF PA; do
    if [ $GAME_TIMESTAMP -ge $dayNow ] ; then
      echo "GAME_ID: ${GAME_ID}" >> /tmp/whoscoming.log
      break;
    fi;
         # sort by GAME_TIMESTAMP
  done < <(sort -t~ -k2,2 -n ${SCHEDULE})
fi

IFS=$' \t\n'
. functions
. attendance.func

cgiVars

htmlHeader

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|TAB_ATTENDANCE|active|" template-header.html

printBootAttendancePage admin ${CGI_action}
cat template-footer.html
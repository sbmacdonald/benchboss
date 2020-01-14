#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions

# pull in the parameters
cgiVars

. forms

LOG_FILE="$(getLogFile $BASH_SOURCE)"

. league.dat
# what is the timestamp of today @ 0:00
dayNow=$(date -d"0:00" +%s)

# look for the first entry in the schedule that is greater than 'dayNow'
if [ "${CGI_gid}" != "" ] ; then
  IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT < <(grep ${CGI_gid} ${SCHEDULE})
else
  IFS='~'
  while read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT; do
    if [ $GAME_TIMESTAMP -ge $dayNow ] ; then
      break;
    fi;
        # sort by GAME_TIMESTAMP
  done < <(sort -t~ -k2,2 -n ${SCHEDULE})
  IFS=$ofigIFS
fi

IFS=$' \t\n'

# pickup the roster functions
. functions
. rsvp.func


logInfo "sGAME_ID: $GAME_ID; _action: $CGI_action;  sCGI_plist: $CGI_plist" >> ${LOG_FILE}
case $CGI_action in
  coming)
    coming
    ;;
  out)
    notComing
    ;;
  request)
    request
    ;;
  rec)
    recinded
    ;;    
esac

htmlHeader

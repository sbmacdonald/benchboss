#!/bin/bash
#
#

. league.dat
. /home/www/cgi-bin/include/functions
cgiVars

# what is the timestamp of today @ 0:00
dayNow=$(date -d"0:00" +%s)

if [ "${CGI_gameId}" != "" ] ; then
  IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT < <(grep "${CGI_gameId}" ${SCHEDULE})
  #echo "$GAME_ID $GAME_TIMESTAMP $GAME_DAY $GAME_START" >> /tmp/whoscoming-divs.input
  echo "{CGI_gameId} ${CGI_gameId}"
else
  # look for the first entry in the schedule that is greater than 'dayNow'
  IFS='~'
  while read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT; do
    if [ $GAME_TIMESTAMP -ge $dayNow ] ; then
      echo "GAME_ID: ${GAME_ID}" >> /tmp/whoscoming.log
      break;
    fi;
         # sort by GAME_TIMESTAMP
  done < <(sort -t~ -k2,2 -n ${SCHEDULE})
fi

IFS=$' \t\n'

. functions
. invite.func

leagueLogFile="${DATA_DIR}/leagueInfo.log"

cgiVars

  debugFile="/tmp/invite-${LEAGUE_ACRO}.cgi"
  chmod 777 $debugFile
  echo "---------------------------------------" >> $debugFile
  date >> $debugFile
  echo "plist:  $CGI_plist" >> $debugFile
  echo "HTTP_REFERER: $HTTP_REFERER" >> $debugFile

resendInvitationEmails


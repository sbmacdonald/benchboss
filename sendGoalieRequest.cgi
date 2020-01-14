#!/bin/bash
#
# $Id: send-invite,v 1.2 2006/11/29 16:22:41 scottm Exp $
#

. league.dat
. /home/www/cgi-bin/include/functions
cgiVars

. admin/functions
. data/league.cfg

# Get the game details from the given CGI_gid
IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE < <(grep "$CGI_gid" ${SCHEDULE})

htmlHeader
#leagueHeader

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" template-header.html

rsvpLogFile="${MAIL_DIR}/rsvp.log"

if [ $CGI_token == ${AdminToken} ] && [ "${emailStatus}" == "enabled" ] ; then

  # only send request emails to spare goalies that have not yet responded
  grep "~[s]~g~[c|u]$" ${ROSTER} | sort -t~ -k1 | awk -F~ '{print $1}' > ${DATA_DIR}/sir
  sort -t~ -k2 ${IN_FILE} ${OUT_FILE} | grep "~[s]~g$" | awk -F~ '{print $2}' > ${DATA_DIR}/sresp

  spares=`comm -23 ${DATA_DIR}/sir ${DATA_DIR}/sresp`

  # Send an invite email to the spares
  sendSpareGoalieEmails ${CGI_reg} "$spares"

  logInfo "spare goalie request emails sent to: $spares" >> ${leagueLogFile}
  logInfo "spare goalie request emails sent to: $spares" >> ${rsvpLogFile}
  echo "<h4>Invite emails sent to the following spare goalies:</h4>"
  echo "<ul>"
  for email in ${spares} ; do
    fname=`getFirstName "$email"`
    lname=`getLastName "$email"`
    echo "<li>$fname $lname ($email)</li>"
  done
  echo "</ul>"
else
  logWarning "basename $0 .cgi called without auth token" >> ${leagueLogFile}
  logWarning "basename $0 .cgi called without auth token" >> ${rsvpLogFile}
  echo "<h3>Authorization Required</h3>"
fi
cat template-footer.html


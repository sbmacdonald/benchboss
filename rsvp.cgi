#!/bin/bash
#
#

. league.dat
. /home/www/cgi-bin/include/functions
cgiVars

. admin/functions

echo "CGI_gid ${CGI_gid}" >> /tmp/rsvp.log

# Only do something if we have an email address in the query parameters
if [ "$CGI_email" != "" ] ; then

  # Get the game details from the given CGI_gid
  IFS='~' read -r GAME_ID GAME_TIMESTAMP GAME_DAY GAME_START GAME_LOCATION GAME_END GAME_ACTIVE OPPONENT PTSF PTSA< <(grep "${CGI_gid:-XXXX9999YYyyY}" ${SCHEDULE})

  echo "id:$GAME_ID ts:$GAME_TIMESTAMP gd:$GAME_DAY gs:$GAME_START gl:$GAME_LOCATION ge:$GAME_END ga:$GAME_ACTIVE" >> /tmp/rsvp.log
  # Grab the first name of the person who has responded 
  firstName=`getFirstName $CGI_email`

  # who has responded ?
  lockfile rsvp.lock
  result=`eval im_${CGI_action} "$CGI_email"`
  rm -r rsvp.lock
  
  htmlHeader

case $result in
  
  beer-confirmed)
      logInfo "im_${CGI_action}(self): $CGI_email" >> ${attendanceLogFile}
      
      . admin/attendance.func
      sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
          -e "s|USERNAME|$REMOTE_USER|g" \
          -e "s|TAB_ATTENDANCE|active|" template-header.html

      printBootAttendancePage public beer-confirmed
      cat template-footer.html
    ;;
   
  beer-too-late)
    logInfo "im_${CGI_action}(self-too-late): $CGI_email" >> ${attendanceLogFile}

    source admin/attendance.func
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html

    printBootAttendancePage public beer-too-late
    cat template-footer.html
    ;;
  
  gameOver)
    logInfo "im_${CGI_action}(self): $CGI_email result: ${result}" >> ${attendanceLogFile}
    #leagueHeader
    
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html
    echo "<br><h5 style=\"margin: 0px;;\"><span style=\"display:block;width:25%\" class=\"alert alert-error\">"
    echo "Sorry $firstName, <br>this game has passed, please wait for the next email"
    echo "</span></h5><br>"
    cat template-footer.html
    ;;
    
  removeMe)
    logInfo "im_${CGI_action}(self): $CGI_email" >> ${attendanceLogFile}
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html
    echo "<br><h5 style=\"margin: 0px;\"><span class=\"alert alert-success\">"
    echo "$firstName, you have been removed from the ${EmailAccountName} RSVP system"
    echo "</span></h5><br>"
    cat template-footer.html
    ;;

  attendance)
    logInfo "im_${CGI_action}(self): $CGI_email" >> ${attendanceLogFile}
    . admin/attendance.func
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html
    printBootAttendancePage public att
    cat template-footer.html
    exit
    ;;

  out)
    # The administrator said that this person was "out"
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html

    if [ "${CGI_src}" != "" ] ; then
      logInfo "im_out(admin-out): $CGI_email" >> ${attendanceLogFile}
      if [ `isRegularGoalie $CGI_email` -eq 0 ] ; then
        if [ "${manageGoalies}" == "true" ] && 
           [ `getSpareGoalieCount` -gt 0 ] ; then
          
          printf "<br><h5 style=\"margin: 0px;\"><span style=\"display:block; width:25%;\"class=\"alert alert-info\">"
          printf "Spare goalies have been contacted.<br>"
          printf "You'll be notified when a keeper is found."
          printf "</span></h5>"
          printf "<meta http-equiv=\"Refresh\" content=\"3; url=attendance.html\">\n"
          printf "</html>\n"
          exit
        fi        
      fi
    else
      logInfo "im_out(self-out): $CGI_email" >> ${attendanceLogFile}
      #leagueHeader
      sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
          -e "s|USERNAME|$REMOTE_USER|g" \
          -e "s|TAB_ATTENDANCE|active|" template-header.html
  
      echo "<br><h5 style=\"margin: 0px;\"><span style=\"display:block; width:25%;\"class=\"alert alert-info\">"
      echo "You've been marked as \"not coming\".<br>" 
      if [ `isSkater $CGI_email` -eq 0 ] ; then
        echo "Thanks for letting us know $firstName !<br>"
      fi
      if [ `isRegularGoalie $CGI_email` -eq 0 ] ; then
        if [ "${manageGoalies}" == "true" ] && 
           [ `getSpareGoalieCount` -gt 0 ] ; then
          echo "<br>Spare goalies have been contacted on your behalf.<br><br>"
          echo "We'll let you know if one of them is able to play."
        else
          echo "<br>A notification email has been sent to the League Organizer."
        fi
      fi
      echo "</span></h5>"
    fi
    cat template-footer.html
    ;;

  rescinded)
    #leagueHeader
    logInfo "im_${CGI_action}(self-recinded): $CGI_email" >> ${attendanceLogFile}
    
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html
    
    echo "<br><h5 style=\"margin: 0px;\"><span style=\"display:block; width:25%;\" class=\"alert alert-success\">"
    echo "$firstName, <br>you've been marked as \"not coming\" <br>Thanks for updating your status"
    if [ `isRegularGoalie $CGI_email` -eq 0 ] ; then
      if [ "${manageGoalies}" == "true" ] && 
         [ `getSpareGoalieCount` -gt 0 ] ; then
        echo "Spare goalies have been contacted on your behalf.<br><br>"
        echo "We'll let you know if one of them is able to play."
      else
        echo "An email has been sent to the League Organizer ${LeagueOrganizer}."
      fi
    fi
    echo "</h4>"

    cat template-footer.html
    ;;

  full)
    #leagueHeader
    logInfo "im_${CGI_action}(self-full): $CGI_email" >> ${attendanceLogFile}

    source admin/attendance.func
    sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
        -e "s|USERNAME|$REMOTE_USER|g" \
        -e "s|TAB_ATTENDANCE|active|" template-header.html

    printBootAttendancePage public full
    cat template-footer.html
    
    ;;

  confirmed)
    # The administrator said that this person was "out"
      #leagueHeader
      logInfo "im_${CGI_action}(self): $CGI_email" >> ${attendanceLogFile}
      
      . admin/attendance.func
      sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
          -e "s|USERNAME|$REMOTE_USER|g" \
          -e "s|TAB_ATTENDANCE|active|" template-header.html
      
      printBootAttendancePage public confirmed
      cat template-footer.html

    ;;

  filled)
    logInfo "im_${CGI_action}(self-filled): $CGI_email" >> ${attendanceLogFile}
    leagueHeader
    echo "<br><h5 style=\"margin: 0px;\"><span style=\"display:block; width:25%;\" class=\"alert alert-error\">"
    echo "$firstName, thanks for responding,<br>"
    echo "Unfortunately we have already found a spare goalie.<br>"
    echo "If we need another goalie, we'll send another email."
    echo "</span></h5>"
    ;;

  failed)
    leagueHeader
    logInfo "im_${CGI_action}(self-failed): $CGI_email" >> ${attendanceLogFile}
    echo "An error occurred.  Contact ${LeagueOrganizer} via email"
    mail -s "${LEAGUE_ACRO} error" scottmac13@gmail.com benoit@xdal.org << EOE
Some error happened with in/out.  Check the error logs.  Here is the info:

$QUERY_STRING
EOE
      ;;
  esac

#leagueFooter

fi


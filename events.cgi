#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. admin/events.func

cgiVars

htmlHeader
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" template-header.html

# Grab the first name of the person who has responded 
firstName=`getFirstName $CGI_email`

# Only do something if we have an email address in the query parameters
if [ "${CGI_id}" != "" ] ; then

  touchEventFiles ${CGI_id}
  chmod -f 777 ${eventsLogFile}

  # who has responded ?
  result=`eval im_${CGI_action} "$CGI_email"`
  echo "$result" >> /tmp/events.log
  case $result in
    eventOver)
      logInfo "im_${CGI_action}(self): $CGI_email result: ${result}" >> ${eventsLogFile}
      
      echo "<h4 style=\"color:red;\">"
      echo "Event \"${CGI_id}\" not found.</h4>"
      logInfo "im_${CGI_action}(self-failed): $CGI_email" >> ${eventsLogFile}
      
      mail -s "${LEAGUE_ACRO} error" scottmac13@gmail.com << EOE
"${LEAGUE_DIR}/events.html" event not found:

QUERY_STRING:$QUERY_STRING
ENV:
`env`
EOE
      ;;
    
    attendance)
      logInfo "im_${CGI_action}(self): $CGI_id" >> ${eventsLogFile}
      printEventPage ${CGI_id}
      ;;

    out)
      logInfo "im_out(self-out): $CGI_email" >> ${eventsLogFile}
      echo "<h4>$firstName you've been marked as \"not coming\".</h4>"
      ;;

    rescinded)
      logInfo "im_out(self-out): $CGI_email" >> ${eventsLogFile}
      echo "<h4>"
      echo "$firstName you've been marked as \"not coming\".</h4>"
      ;;

    confirmed)
      logInfo "im_${CGI_action}(self): $CGI_email" >> ${eventsLogFile}
      
      echo "<h4 style=\"color:green;\">"
      echo "$firstName, you're confirmed !</h4>"
      printEventPage ${CGI_id}
      ;;

    failed)
      logInfo "im_${CGI_action}(self-failed): $CGI_email" >> ${eventsLogFile}
      echo "<h4 style=\"color:red;\">An error occurred.  Contact ${LeagueOrganizer} via email</h4>"
      mail -s "${LEAGUE_ACRO} error" scottmac13@gmail.com << EOE
"${LEAGUE_DIR}/events.html"  Error occrre:

QUERY_STRING: $QUERY_STRING
ENV:
`env`
EOE
      ;;
  esac

else
  logInfo "events.cgi: no action supplied" >> ${eventsLogFile}
  echo "<h4 style=\"color:red;\">Event not found.  Contact ${LeagueOrganizer} via email</h4>"
  mail -s "${LEAGUE_ACRO} error" scottmac13@gmail.com << EOE
"${LEAGUE_DIR}/events.html" accessed without eventId:

QUERY_STRING: $QUERY_STRING
ENV:
`env`
EOE

fi

cat template-footer.html

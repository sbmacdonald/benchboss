#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. functions
. groupMail.func

LOG_FILE="$(getLogFile $BASH_SOURCE)"

leagueLogFile="${DATA_DIR}/leagueInfo.log"

cgiVars

logInfo "action: $CGI_action  plist: $$CGI_plist HTTP_REFERER: $HTTP_REFERER" >> ${LOG_FILE}

# Pick up the new values
. $LEAGUE_CFG

# Handle the action appropriately
if [ ! -z ${CGI_action} ] ; then
  case "$CGI_action" in
   success)
         
     printSuccessPage
     ;;
        
   send)
     sendMail
     ;;
  esac
else
     printMailForm
fi


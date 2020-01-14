#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. forms

# pickup the roster functions
. roster-rsi.func

# pull in the parameters
cgiVars

echo "CGI_action: $CGI_action" >> /tmp/player.cgi.input
echo "CGI_plist: $CGI_plist" >> /tmp/player.cgi.input
chmod 777 /tmp/player.cgi.input

case $CGI_action in
  add)
    printPlayerForm
    ;;
  edt)
    printPlayerInfoForm
    ;;
  mtr)
    moveToRegulars
    ;;
  mts)
    moveToSpares
    ;;
  mti)
    moveToInactive
    ;;
  mtd)
    deletePlayer
    ;;
  mtc)
    # player has been moved to confirmed
    moveToConfirmed
    ;;
  mta)
    moveToBeerDuty
    ;;
  mte)
    moveToBeerDutyExemptions
    ;;
  reconfirm)
    reconfirm
    ;;    
esac

htmlHeader

#!/bin/bash

. /home/www/cgi-bin/include/functions
. events.func

cgiVars


# ---------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------- 
htmlHeader

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|TAB_ADMIN|active|" template-header.html

case "$CGI_action" in
  main)
    printMainPage
    ;;
  new)
    printEventForm
    ;;
  create)
    createEvent
    ;;
  disp)
    printEventPage ${CGI_id} admin
    ;;
  mti)
    moveToIn
    ;;
  mto)
    moveToOut
    ;;
esac

cat template-footer.html

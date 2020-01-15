#!/bin/bash

. /home/www/cgi-bin/include/functions
. events.func

cgiVars


# ---------------------------------------------------------------------------- 
# ---------------------------------------------------------------------------- 
htmlHeader

# Some LeagueTypes don't have goalies, so we hide the
# goalie admin menu item
case ${LeagueType} in
  Hockey|Soccer)admin_goalie="display:"; ;;
  *)admin_goalie="display:none"; ;;
esac

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|ADMIN_GOALIES|${admin_goalies}|g" \
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

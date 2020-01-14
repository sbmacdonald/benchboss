#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. forms

cgiVars

echo "CGI_action: $CGI_action" >> /tmp/addPlayer.cgi.input
echo "CGI_Action: $CGI_Action" >> /tmp/addPlayer.cgi.input
chmod 777 /tmp/addPlayer.cgi.input

htmlHeader
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|MENU_1|active|" template-header.html

printPlayerInfoFormDivs

cat template-footer.html
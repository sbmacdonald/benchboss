#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. functions

htmlHeader
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ROSTER|active|" template-header.html

#registrationHeader

printGotItPage

cat template-footer.html

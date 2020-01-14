#!/bin/bash
. /home/www/cgi-bin/include/functions
. functions

cgiVars
. ${DATA_DIR}/league.cfg


. confirm.func

cgiVars

htmlHeader

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|${REMOTE_USER}|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|g" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|TAB_ROSTER|active|g" template-header.html

printBulkConfirmPage ${CGI_action}

cat template-footer.html

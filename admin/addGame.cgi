#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. forms

cgiVars

echo "CGI_action: $CGI_action" >> /tmp/addGame.cgi.input
echo "CGI_Action: $CGI_Action" >> /tmp/addGame.cgi.input
chmod 777 /tmp/addGame.cgi.input

htmlHeader
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|ADMIN_TAB|active|" template-header.html

case ${CGI_action} in
  edt)
    printGameInfoForm
    ;;
  add)
    printGameInfoForm
    ;;
  score)
    printScoreEntryForm
    ;;
esac

cat template-footer.html
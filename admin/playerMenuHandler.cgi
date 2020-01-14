#!/bin/bash

. functions
. ${DATA_DIR}/league.cfg

cgiVars


touch /tmp/playerMenuHandler.log
chmod 777 /tmp/playerMenuHandler.log
env >> /tmp/playerMenuHandler.log

case $CGI_action in
    mts)
      printf "mts: $CGI_player\n" >> /tmp/playerMenuHandler.log
      ;;
    mtr)
      printf "mtr: $CGI_player\n" >> /tmp/playerMenuHandler.log
      ;;
      *)
      printf "unknown: $CGI_player\n" >> /tmp/playerMenuHandler.log      
      ;;
esac

cat << EOF
Status: 302 redirect
Location: bulkRoster.cgi

EOF
exit

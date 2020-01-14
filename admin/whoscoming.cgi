#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. functions

chmod 777 ${attendanceLogFile}

cgiVars

# Check to see if we are doing something more than displaying the page 
if [ "$CGI_action" != "" -a "$CGI_email" != "" ] ; then
  #printf "%s %s\n" "$CGI_email" "$CGI_action"
  case $CGI_action in
    in)
      result=`im_in "$CGI_email"`
      logInfo "im_in($REMOTE_USER): $CGI_email" >> ${attendanceLogFile}
      #printf "adding %s\n" "$CGI_email"
      ;;
    out)
      result=`im_out "$CGI_email"`
      logInfo "im_out($REMOTE_USER): $CGI_email" >> ${attendanceLogFile}
      #printf "removing %s\n" "$CGI_email"
      ;;
  esac
cat <<EOF
Status: 302 redirect
Location: whoscoming.cgi

EOF
exit
fi

htmlHeader

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ATTENDANCE|active|" template-header.html

#attendanceHeader
printAttendancePage
#htmlFooter
cat template-footer.html
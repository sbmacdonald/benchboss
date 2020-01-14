#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. admin/functions

attendanceLogFile="${DATA_DIR}/attendance.log"
chmod 777 ${attendanceLogFile}

cgiVars

# Check to see if we are doing something more than displaying the page 
if [ "$CGI_action" != "" -a "$CGI_email" != "" ] ; then
  #printf "%s %s\n" "$CGI_email" "$CGI_action"
  case $CGI_action in
    in)
      result=`im_in "$CGI_email"`
      logInfo "im_in(admin): $CGI_email" >> ${attendanceLogFile}
      #printf "adding %s\n" "$CGI_email"
      ;;
    out)
      result=`im_out "$CGI_email"`
      logInfo "im_out(admin): $CGI_email" >> ${attendanceLogFile}
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
attendanceHeader
printPublicAttendancePage
htmlFooter

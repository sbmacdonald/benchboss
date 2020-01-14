#!/bin/bash
#
#
. /home/www/cgi-bin/include/functions
. admin/functions
. data/league.cfg
. league.data

cgiVars

htmlHeader

file="${DATA_DIR}/registration.log"
#chmod 777 $file
memberfname=`getFirstName $CGI_email`
memberlname=`getLastName $CGI_email`

printResponseRecord "$CGI_email" >> $file

alreadyConfirmed=`grep $CGI_email ${ROSTER} | awk -F~ '{print $6}'`

firstName=`getFirstName $CGI_email`

# update the roster file
sed -i "s|\(${CGI_email}~.*\)\(~[u|c]\)|\1~c|" ${ROSTER}

sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ATTENDANCE|active|" template-header.html
echo "<h4 style=\"color:green\">"
echo "$firstName, you are confirmed with the ${EmailAccountName} RSVP System!</h4>"
cat template-footer.html


htmlFooter

# only send the email the first time the player confirms
if [ "${alreadyConfirmed}" != "c" ] ; then

# send an email to scott to let him know that somebody "got it"
mail -s "${LEAGUE_DIR} Registration Confirmed" ${EmailAccountAddress} -- -f"benchboss@xdal.org" -F"BenchBoss" <<EOF
${LEAGUE_DIR}: $memberfname $memberlname $CGI_email  has been CONFIRMED.
EOF

fi
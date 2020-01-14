#!/bin/bash
#
#

. functions
. admin.func

cgiVars
. ${DATA_DIR}/league.cfg

if [ ! -z ${CGI_section} ] ; then
  chmod 777 $leagueLogFile

  case "$CGI_section" in

    regularsConfirm)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Regulars emails:" >> $leagueLogFile
      sed -i "s|^regularsEmailDay.*|regularsEmailDay=\"$CGI_regularsDay\"|g" $LEAGUE_CFG
      sed -i "s|^regularsEmailTime.*|regularsEmailTime=\"$CGI_regularsTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_regularsDay} ${CGI_regularsTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_ACRO}_DIR/send-invite regulars"
      printf "From: ${EmailAccountAddress}\nSubject: Regulars Confirm Crontab change\nPlease change the regulars cron to: $newEntry\n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*regularsConfirm.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-invite regulars|" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev 
      chmod 777 /tmp/crontab.www-data
    ;;

    regularsReminder)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Regulars Reminder emails:" >> $leagueLogFile
      sed -i "s|^regularsReminderFlag.*|regularsReminderFlag=\"$CGI_regularsReminder\"|g" $LEAGUE_CFG
      sed -i "s|^regularsReminderEmailDay.*|regularsReminderEmailDay=\"$CGI_regularsReminderDay\"|g" $LEAGUE_CFG
      sed -i "s|^regularsReminderEmailTime.*|regularsReminderEmailTime=\"$CGI_regularsReminderTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_regularsReminderDay} ${CGI_regularsReminderTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_ACRO}_DIR/send-invite reminders"
      printf "From: ${EmailAccountAddress}\nSubject: Regulars Reminder Crontab change\nPlease change the regulars reminder cron to: $newEntry\n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*regularsReminder.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-reminder regulars|" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev 
      chmod 777 /tmp/crontab.www-data
    ;;

    spares)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Spares emails:" >> $leagueLogFile
      sed -i "s|^sparesEmailDay.*|sparesEmailDay=\"$CGI_sparesDay\"|g" $LEAGUE_CFG
      sed -i "s|^sparesEmailTime.*|sparesEmailTime=\"$CGI_sparesTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_sparesDay} ${CGI_sparesTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_ACRO}_DIR/send-invite spares"
      printf "From: ${EmailAccountAddress}\nSubject: Spares Crontab change\nPlease change the spares cron to: $newEntry \n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*spares.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-invite spares|" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev
      chmod 777 /tmp/crontab.www-data
    ;;
  esac
fi

# Pick up the new values
. $LEAGUE_CFG

# Compute emailStatus radio buttons
emailStatusSelection=""
if [ "${emailStatus}" == "enabled" ] ; then
  emailStatusSelection+="<input style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"enabled\" checked=\"checked\"/> Enabled"
  emailStatusSelection+="<br><input style=\"margin: 0;\"type=\"radio\" name=\"emailStatus\" value=\"disabled\" /> Disabled"
else
  emailStatusSelection+="<input class=\"input-small\" style=\"margin: 0;\" style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"enabled\"/> Enabled"
  emailStatusSelection+="<br><input style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"disabled\"  checked=\"checked\"/> Disabled"
fi

# Compute the Regulars Email Day Selection 
regularsEmailSelection=""
for day in Sun Mon Tue Wed Thu Fri Sat ; do
  if [ "${regularsEmailDay}" == "$day" ] ; then
    regularsEmailSelection+="<option value=\"$day\" selected>$day</option>"
  else
    regularsEmailSelection+="<option value=\"$day\">$day</option>"
  fi
done

# Compute Regulars Reminder Email checkbox
regularReminderSelection="<input style=\"margin:0px;\" type=\"checkBox\" name=\"regularsReminder\" "
if [ "${regularsReminderFlag}" == "true" ] ; then
  regularReminderSelection+="value=\"true\" checked=\"checked\"/> "
else
  regularReminderSelection+="value=\"true\"/> "
fi
#regularReminderSelection+="Send reminder email every:"

# Compute the Regulars Reminder Email Day Selection 
regularsEmailTitle="Day & Time when the first confirmation emails are send to all regulars"
regularsReminderEmailTitle="Send a second (reminder) confirmation email to "
regularsReminderEmailTitle+="regulars who have not yet responded.  Typically "
regularsReminderEmailTitle+="this should be *before* the spares emails are sent."
regularsReminderEmailSelection=""
for day in Sun Mon Tue Wed Thu Fri Sat ; do
  if [ "${regularsReminderEmailDay}" == "$day" ] ; then
    regularsReminderEmailSelection+="<option value=\"$day\" selected>$day</option>"
  else
    regularsReminderEmailSelection+="<option value=\"$day\">$day</option>"
  fi
done

# Compute the Spares Email Day Selection 
sparesEmailTitle="Day & time when the invitation emails are sent to all spares"
sparesEmailSelection=""
for day in Sun Mon Tue Wed Thu Fri Sat ; do
  if [ "${sparesEmailDay}" == "$day" ] ; then
    sparesEmailSelection+="<option value=\"$day\" selected>$day</option>"
  else
    sparesEmailSelection+="<option value=\"$day\">$day</option>"
  fi
done

# Start building the web page that will be displayed
htmlHeader

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|TAB_ADMIN|active|" template-header.html

cat<<EIEIO

<table>

<!-- RSVP Email Status -->
<tr>
<td>
  <fieldset>
  <legend>RSVP/Invite Email Status:</legend>
  <form action="rsvpAdmin.cgi" method="POST">
    <table>
      <tr><td style="text-align:right"><b>Email Status:</b></td>
          <td> ${emailStatusSelection} </td>
      
      <td>&nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value="Update" /> </td>
      </tr>
    </table>
  </form>
<td>
<tr>
<!-- Regulars (RSVP) Emails -->
<tr>
<td >
  <fieldset>
  <legend >Regulars (RSVP) Emails:</legend>
  <form action="rsvpAdmin.cgi" method="POST">
    <input name="section" value="regularsConfirm" type="hidden">
    <table>
      <tr><td class="" title="$regularsEmailTitle"><b>Send initial email every:</b></td></tr>
      <tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<select class="input-small" name="regularsDay">${regularsEmailSelection}</select>
           at: <input class="input-small" name="regularsTime" type="text" id="regularsTime" value="${regularsEmailTime}"></td></tr>
      <tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value="Update" /> 
      </td></tr>
    </table>
  </form>
  <form action="rsvpAdmin.cgi" method="POST">
    <input name="section" value="regularsReminder" type="hidden">
    <table>
      <tr><td title="$regularsReminderEmailTitle"><b>
           ${regularReminderSelection}Send reminder email every:</b></td></tr>
      <tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<select class="input-small" name="regularsReminderDay">${regularsReminderEmailSelection}</select>
           at: <input class="input-small" name="regularsReminderTime" type="text" size="6" 
                 id="regularsReminderTime" value="${regularsReminderEmailTime}"></td></tr>
      <tr><td>
          &nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value="Update" /> </td></tr>
      <td></td>
    </table>
  </form>
  </fieldset>
</td>
</tr>
<!-- Spares (Invite) Emails -->
<tr>
<td>
<form action="rsvpAdmi.cgi" method="POST">
<fieldset>
<legend>Spares (Invitation) Emails:</legend>
<input name="section" value="spares" type="hidden">
<table>
<tr>
  <td title="${sparesEmailTitle}"><b>Send email every:</b></td></tr>
<tr>
  <td>&nbsp;&nbsp;&nbsp;&nbsp;<select class="input-small" name="sparesDay">${sparesEmailSelection}</select>
   at: <input class="input-small" name="sparesTime" type="text" id="sparesTime" value="${sparesEmailTime}"><td></tr>
  <tr><td>&nbsp;&nbsp;&nbsp;&nbsp;<input type="submit" value="Update" /></td></tr>
</tr></table>
</fieldset>
</form>
</td>
</tr>

</table>
EIEIO

cat template-footer.html
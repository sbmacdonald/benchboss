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
  
    emailStatus)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating email status From: $emailStatus" >> $leagueLogFile
      logInfo "[$REMOTE_USER]: Updating email status To: $CGI_emailStatus" >> $leagueLogFile
      sed -i "s|^emailStatus.*|emailStatus=\"$CGI_emailStatus\"|g" $LEAGUE_CFG
      ;;      

    regulars)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Regulars emails From: regularsEmailDay=$regularsEmailDay regularsEmailTime=$regularsEmailTime " >> $leagueLogFile
      logInfo "[$REMOTE_USER]: Updating Regulars emails To:   regularsEmailDay=$CGI_regularsDay regularsEmailTime=$CGI_regularsTime " >> $leagueLogFile
      
      sed -i "s|^regularsEmailDay.*|regularsEmailDay=\"$CGI_regularsDay\"|g" $LEAGUE_CFG
      sed -i "s|^regularsEmailTime.*|regularsEmailTime=\"$CGI_regularsTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_regularsDay} ${CGI_regularsTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_DIR}_DIR/send-invite regulars"
      printf "From: ${EmailAccountAddress}\nSubject: Regulars Confirm Crontab change\nPlease change the regulars cron to: $newEntry\n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*regularsConfirm.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-invite regulars|" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev 
      chmod 777 /tmp/crontab.www-data
      
      logInfo "[$REMOTE_USER]: Updating Regulars Reminder emails From: regularsReminderFlag=$regularsReminderFlag regularsReminderEmailDay=$regularsReminderEmailDay regularsReminderEmailTime=$regularsReminderEmailTime" >> $leagueLogFile
      logInfo "[$REMOTE_USER]: Updating Regulars Reminder emails To:   regularsReminderFlag=$CGI_regularsReminder regularsReminderEmailDay=$CGI_regularsReminderDay regularsReminderEmailTime=$CGI_regularsReminderTime" >> $leagueLogFile
      sed -i "s|^regularsReminderFlag.*|regularsReminderFlag=\"$CGI_regularsReminder\"|g" $LEAGUE_CFG
      sed -i "s|^regularsReminderEmailDay.*|regularsReminderEmailDay=\"$CGI_regularsReminderDay\"|g" $LEAGUE_CFG
      sed -i "s|^regularsReminderEmailTime.*|regularsReminderEmailTime=\"$CGI_regularsReminderTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_regularsReminderDay} ${CGI_regularsReminderTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_DIR}_DIR/send-invite reminders"
      printf "From: ${EmailAccountAddress}\nSubject: Regulars Reminder Crontab change\nPlease change the regulars reminder cron to: $newEntry\n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*regularsReminder.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-reminder regulars|" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev 
      chmod 777 /tmp/crontab.www-data
    ;;

    spares)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Spares emails From: sparesEmailDay=$sparesEmailDay sparesEmailTime=$sparesEmailTime" >> $leagueLogFile
      logInfo "[$REMOTE_USER]: Updating Spares emails From: sparesEmailDay=$CGI_sparesDay sparesEmailTime=$CGI_sparesTime" >> $leagueLogFile
      sed -i "s|^sparesEmailDay.*|sparesEmailDay=\"$CGI_sparesDay\"|g" $LEAGUE_CFG
      sed -i "s|^sparesEmailTime.*|sparesEmailTime=\"$CGI_sparesTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_sparesDay} ${CGI_sparesTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_DIR}_DIR/send-invite spares"
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
  emailStatusOptions="<option value=\"disabled\">disabled</option><option value=\"enabled\" selected>enabled</option>"
else
  emailStatusOptions="<option value=\"disabled\" selected>disabled</option><option value=\"enabled\">enabled</option>"
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

<!-- RSVP Email Status -->
<div class="row-fluid" style="padding:15px 0px 10px 0px;">
  <div class="span4 bubble-fieldset" >
  <legend>RSVP/Invite Email Status:</legend>
  <form action="rsvpAdmin-divs.html" method="POST" class="form-inline form-indent" style="padding-left: 0px;">
    <input name="section" value="emailStatus" type="hidden"/>
        <label for="flip-1"><b>Email Status:</b></label>
        <select name="emailStatus" id="emailStatus" class="input-small">
        ${emailStatusOptions}
        </select>
        <button type="submit" class="btn btn-primary">Update</button>
    <!-- </div>  /class="control-group"-->
  </form>
  </div> <!-- /style="background-color: -->
</div> <!-- /class="row-fluid" -->

<!-- Regulars (RSVP) Emails -->
<div class="row-fluid" style="padding:0px 0px 10px 0px;">
  <div class="span4 bubble-fieldset" >
  <legend >Regulars (RSVP) Emails:</legend>
  <form action="rsvpAdmin-divs.html" method="POST" class="form-inline form-indent" style="padding-left: 0px;">
    <input name="section" value="regulars" type="hidden">
    <label for="regularsDay"><b>Send initial email every:</b></label><br>
      <div style="padding-left: 20px;">
        <div class="input-prepend"><span class="add-on"><i class="icon-calendar" ></i></span>
        <select class="input-small" name="regularsDay">${regularsEmailSelection}</select> </div> <b>at:</b> 
        <div id="regularTimePicker" class="input-prepend"><span class="add-on"><i class="icon-time" ></i></span>
        <input readonly type="text" style="background-color: #ffffff;cursor: pointer;" data-format="HH:mm PP" class="input-mini add-on-target" name="regularsTime" size="8" id="regularsTime" value="${regularsEmailTime:-9:00 AM}"/></div>
      </div>
           <div style="padding:10px 0px 10px 0px;">
           <b>${regularReminderSelection}Send reminder email every:</a></b><br>
           <!-- indent the input line -->
           <div style="padding-left: 20px; padding-top:10px;">
      <div class="input-prepend"><span class="add-on"><i class="icon-calendar" ></i></span>
      <select class="input-small" name="regularsReminderDay">${regularsReminderEmailSelection}</select></div> 
           <b>at:</b>
      <div id="reminderTimePicker" class="input-prepend"><span class="add-on"><i class="icon-time" ></i></span>
           <input readonly style="background-color: #ffffff;cursor: pointer;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="regularsReminderTime"  
                 id="regularsReminderTime" size="8" value="${regularsReminderEmailTime:-9:00 AM}"/></div>
      </div>
      </div>
      <button type="submit" class="btn btn-primary">Update</button> 
  </form>
</div>
</div>

<!-- Spares (Invite) Emails -->
<div class="row-fluid" style="padding:0px 0px 10px 0px;">
  <div class="span4 bubble-fieldset" >
    <form action="rsvpAdmin-divs.html" method="POST" class="form-inline form-indent" style="padding-left:0px;">
      <legend>Spares (Invitation) Emails:</legend>
      <input name="section" value="spares" type="hidden">
      <label for="sparesDay"><b>Send email every:</b></label><br>
      <div style="padding-left:20px;">
      <div class="input-prepend">
        <span class="add-on"><i class="icon-calendar" ></i></span>
        <select class="input-small" name="sparesDay">${sparesEmailSelection}</select>
      </div>
      <b>at:</b>
      <div id="spareTimePicker" class="input-prepend">
        <span class="add-on"><i class="icon-time" ></i></span>
        <input readonly style="background-color: #ffffff;cursor: pointer;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="sparesTime" size="8" id="sparesTime" value="${sparesEmailTime:-9:00 AM}"/>
      </div>
      </div>
      <div class="btn-pad-top">
       <button type="submit" class="btn btn-primary">Update</button>
      </div>
    </form>
  </div> <!-- / class="span5 bubble-fieldset" -->
</div>

    
EIEIO

cat template-footer.html
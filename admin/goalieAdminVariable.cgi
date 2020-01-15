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
    goalieCantCome)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Goalie Management from: goalieNotify=${goalieNotify} manageGoalies=${manageGoalies}" >> $leagueLogFile
      sed -i "s|^goalieNotify.*|goalieNotify=\"$CGI_goalieNotify\"|g" $LEAGUE_CFG
      sed -i "s|^manageGoalies.*|manageGoalies=\"$CGI_manageGoalies\"|g" $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Goalie Management To: goalieNotify=$CGI_goalieNotify manageGoalies=$CGI_manageGoalies" >> $leagueLogFile
    ;;

    goalieNoResponse)
      . $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Goalie Management from: goalieNoResponseNotify=${goalieNoResponseNotify} " >> $leagueLogFile
      sed -i "s|^goalieNoResponseNotify.*|goalieNoResponseNotify=\"$CGI_goalieNoResponseNotify\"|g" $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updating Goalie Management To: goalieNoResponseNotify=$CGI_goalieNoResponseNotify " >> $leagueLogFile
      sed -i "s|^goalieNoResponseEmailDay=.*|goalieNoResponseEmailDay=\"$CGI_goalieNoResponseEmailDay\"|g" $LEAGUE_CFG
      sed -i "s|^goalieNoResponseEmailTime=.*|goalieNoResponseEmailTime=\"$CGI_goalieNoResponseEmailTime\"|g" $LEAGUE_CFG
      newEntry=`date "+0 %k * * %a" -d "${CGI_goalieNoResponseEmailDay} ${CGI_goalieNoResponseEmailTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_DIR}_DIR/sendGoalieNoResponse"
      printf "From: ${EmailAccountAddress}\nSubject: Goalie No Response Crontab change\nPlease change the goalies cron to: $newEntry \n\n" | /usr/lib/sendmail scottmac13@gmail.com
      sed "s|.*${LEAGUE_ACRO}.*goalieNoRessponse.*|${newEntry} \$${LEAGUE_ACRO}_DIR/send-goalieNoResponse |" /tmp/crontab.prev > /tmp/crontab.www-data
      #cp /tmp/crontab.www-data /tmp/crontab.prev
      chmod 777 /tmp/crontab.www-data
    ;;
  esac
fi


# --------------------------------------------------------------------
# Pick up the new values
. $LEAGUE_CFG


# Compute goalieNotify checkbox
goalieNotifySelection="<input style=\"margin:0;\" type=\"checkBox\" name=\"goalieNotify\" "
if [ "${goalieNotify}" == "true" ] ; then
  goalieNotifySelection+="value=\"true\" checked=\"checked\"/> "
else
  goalieNotifySelection+="value=\"true\"/> "
fi
goalieNotifySelection+="Send me an email notification"

# Compute manageGoalies checkbox
manageGoaliesTitle="Invitation emails will be send to the list of spare goalies "
manageGoaliesTitle+="as soon as a regular reports that they can not make it. &#013;&#013;"
manageGoaliesTitle+="If this option is disabled, the email notification will "
manageGoaliesTitle+="contain a link that will allow you to send the email to "
manageGoaliesTitle+="the spare goalies."
manageGoaliesSelection="<input style=\"margin:0;\" title=\"$manageGoaliesTitle\" type=\"checkbox\" name=\"manageGoalies\" "
if [ "${manageGoalies}" == "true" ] ; then
  manageGoaliesSelection+="value=\"true\" checked=\"checked\"/> "
else
  manageGoaliesSelection+="value=\"true\"/> "
fi
manageGoaliesSelection+="Automatically send invites to spare goalies"

# Compute the Goalie No Reponse Email Day Selection 
goalieNoResponseEmailSelection=""
for day in 0 1 2 3 4 5 6 ; do
  if [ "${goalieNoResponseEmailDay}" == "$day" ] ; then
    goalieNoResponseEmailSelection+="<option value=\"$day\" selected>$day</option>"
  else
    goalieNoResponseEmailSelection+="<option value=\"$day\">$day</option>"
  fi
done

# Compute goalieNotify checkbox
goalieNoResponseNotifySelection="<input style=\"margin:0;\" type=\"checkBox\" name=\"goalieNoResponseNotify\" "
if [ "${goalieNoResponseNotify}" == "true" ] ; then
  goalieNoResponseNotifySelection+="value=\"true\" checked=\"checked\"/> "
else
  goalieNoResponseNotifySelection+="value=\"true\"/> "
fi
goalieNoResponseNotifySelection+="Send me an email notification"


# Start building the web page that will be displayed
htmlHeader

# Some LeagueTypes don't have goalies, so we hide the
# goalie admin menu item
case ${LeagueType} in
  Hockey|Soccer)admin_goalies="display:"; ;;
  *)admin_goalies="display:none"; ;;
esac

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|ADMIN_GOALIES|${admin_goalies}|g" \
    -e "s|TAB_ADMIN|active|" template-header.html

cat<<EIEIO
<!-- Goalie Management -->
<h4>Goalie Management</h4>
<div class="row-fluid" style="padding:0px 0px 10px 0px;">
  <div class="span4 bubble-fieldset" >
    <form action="goalieAdminVariable.cgi" method="POST" class="form-horizontal">
      <input name="section" value="goalieCantCome" type="hidden">
      <div style="padding-top:10px;"><b>When a regular goalie can't make it:</b></div>
      <div style="padding-left:15px;">
        ${goalieNotifySelection}
      </div>
      <div style="padding-left:15px; padding-top: 5px; padding-bottom:5px;">
        ${manageGoaliesSelection}
      </div>
      <div class="btn-pad-top">
        <button type="submit" class="btn btn-small btn-primary">Update</button>
      </div>
    </form>
  </div>
</div>

<div class="row-fluid" style="padding:0px 0px 10px 0px;">
  <div class="span4 bubble-fieldset btn-pad-top" >
    <form action="goalieAdminVariable.cgi" method="POST" class="form-inline form-indent" style="padding-left:0px;">
      <input name="section" value="goalieNoResponse" type="hidden">
      <label for="goalieNoResponseEmailDay"><b>When a regular goalie doesn't respond by:</b></label><br>
      <div style="padding-left:15px;">
        <b>at:</b>
        <div id="spareTimePicker" class="input-prepend">
          <span class="add-on"><i class="icon-time" ></i></span>
          <input readonly style="background-color: #ffffff;cursor: pointer;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="goalieNoResponseEmailTime"  size="8" id="goalieNoResponseEmailTime" value="${goalieNoResponseEmailTime}"/>:
          </div>
          <select class="input-mini" id="goalieNoResponseEmailDay" name="goalieNoResponseEmailDay">${goalieNoResponseEmailSelection}</select>
          <span id="goalieNoResponseEmailDaysBefore">days before the game</span>
        </div>
        <div style="padding: 10px 0px 10px 0px;">
          ${goalieNoResponseNotifySelection}
        </div>
      <div class="btn-pad-top">
        <button type="submit" class="btn btn-small btn-primary">Update</button>
      </div>
    </form>
  </div>
</div>

EIEIO

cat template-footer.html

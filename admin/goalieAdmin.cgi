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
      newEntry=`date "+0 %k * * %a" -d "${CGI_goalieNoResponseEmailDay} ${CGI_goalieNoResponseTime} - 1 hour"`
      newEntry+=" \$${LEAGUE_ACRO}_DIR/sendGoalieNoResponse"
      printf "From: ${EmailAccountAddress}\nSubject: Goalie No Response Crontab change\nPlease change the spares cron to: $newEntry \n\n" | /usr/lib/sendmail scottmac13@gmail.com
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
for day in Sun Mon Tue Wed Thu Fri Sat ; do
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

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ROSTER|active|" template-header.html

cat<<EIEIO
<!-- Goalie Management -->
<table>
<tr>
<td>
<fieldset>
<legend>Goalie Management:</legend>
<form action="leagueInfo.cgi" method="POST">
<input name="section" value="goalieCantCome" type="hidden">
<table>
  <tr>
    <td class="input-left"><b>When a regular goalie can't make it:</b></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;${goalieNotifySelection}</td>
  </tr>
  <tr>
    <td title="$manageGoaliesTitle">&nbsp;&nbsp;${manageGoaliesSelection}</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;<input type="submit" value="Update" /></td>
  </tr>
</table>
</form>


<form action="leagueInfo.cgi" method="POST">
<input name="section" value="goalieNoResponse" type="hidden">
<table>
  <tr>
    <td class="input-left"><b>When a regular goalie doesn't respond by:</b></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;<select class="input-small" name="goalieNoResponseEmailDay">${goalieNoResponseEmailSelection}</select>
 at: <input class="input-mini" name="goalieNoResponseEmailTime" type="text" size="6" id="goalieNoResponseEmailTime" value="${goalieNoResponseEmailTime}">:</td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;${goalieNoResponseNotifySelection}</td>
    <td></td>
  </tr>
  <tr>
    <td>&nbsp;&nbsp;<input type="submit" value="Update" /></td>
    <td></td>
  </tr>
</table>
</form>

</fieldset>
</td>
</tr>
</table>

EIEIO

cat template-footer.html
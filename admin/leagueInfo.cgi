#!/bin/bash
#
#

. functions
. admin.func

cgiVars
. ${DATA_DIR}/league.cfg

chmod 777 $LEAGUE_CFG

# Depending on the section being upated, assume all values have changed and
# update them
if [ ! -z ${CGI_section} ] ; then
  chmod 777 $leagueLogFile
  case "$CGI_section" in
    info)
      #infoKeys=(gameDay gameStart gameEnd gameLocation emailStatus spareFee maxSpots)
      #for ((i=0; i < ${#infoKeys[@]}; i++)) ; do 
      #  getConfigValue ${infoKeys[$i]} "`eval echo \\\$CGI_${infoKeys[$i]}`" val newVal
      #  if [ $? -eq 1 ] ; then 
      #    key=${infoKeys[$i]}
      #    logInfo "Key '${key}' updated from: '$val' to: '$newVal'" 
      #    sed -i "s|^${key}.*|${key}=\"$newVal\"|g" $LEAGUE_CFG
      #  fi 
      #done
      logInfo "[$REMOTE_USER]: Updating League Info From: ${LeagueOrganizer} ${OrganizerEmail} ${EmailAccountName} ${EmailAccountAddress} ${EmailAccountPass} ${replyToOrganizer} ${gameDay} ${gameStart} ${gameEnd} ${gameLocation} ${emailStatus} ${spareFee} ${maxSpots}" >> $leagueLogFile
      sed -i "s|^LeagueOrganizer.*|LeagueOrganizer=\"$CGI_organizer\"|g" $LEAGUE_CFG
      sed -i "s|^OrganizerEmail.*|OrganizerEmail=\"$CGI_organizerEmail\"|g" $LEAGUE_CFG
      sed -i "s|^EmailAccountName.*|EmailAccountName=\"$CGI_leagueEmailName\"|g" $LEAGUE_CFG
      sed -i "s|^EmailAccountAddress.*|EmailAccountAddress=\"$CGI_leagueEmailAddress\"|g" $LEAGUE_CFG
      sed -i "s|^EmailAccountPass.*|EmailAccountPass=\"$CGI_leagueEmailPwd\"|g" $LEAGUE_CFG
      sed -i "s|^replyToOrganizer.*|replyToOrganizer=\"$CGI_replyToOrganizer\"|g" $LEAGUE_CFG
      sed -i "s|^gameDay.*|gameDay=\"$CGI_gameDay\"|g" $LEAGUE_CFG
      sed -i "s|^gameStart.*|gameStart=\"$CGI_gameStart\"|g" $LEAGUE_CFG
      sed -i "s|^gameEnd.*|gameEnd=\"$CGI_gameEnd\"|g" $LEAGUE_CFG
      sed -i "s|^gameLocation.*|gameLocation=\"$CGI_gameLocation\"|g" $LEAGUE_CFG
      sed -i "s|^emailStatus.*|emailStatus=\"$CGI_emailStatus\"|g" $LEAGUE_CFG
      sed -i "s|^spareFee.*|spareFee=$CGI_spareFee|g" $LEAGUE_CFG
      sed -i "s|^maxSpots.*|maxSpots=$CGI_maxSpots|g" $LEAGUE_CFG
      logInfo "[$REMOTE_USER]: Updated League Info To: $CGI_organizer $CGI_organizerEmail $CGI_leagueEmailName $CGI_leagueEmailAddress $CGI_leagueEmailPwd $CGI_replyToOrganizer $CGI_gameDay $CGI_gameStart $CGI_gameEnd $CGI_gameLocation $CGI_emailStatus $CGI_spareFee $CGI_maxSpots $CGI_maxSpots" >> $leagueLogFile
    ;;

  esac
fi

# Pick up the new values
. $LEAGUE_CFG

# Compute the value for reply-to League Organizer
replyToOrganizerTitle="Any replies to rsvp/invite emails will be sent to the the League Organizer"
replyToOrganizerSelection="<input style=\"margin: 0;\" title=\"$replyToOrganizerTitle\" type=\"checkBox\" name=\"replyToOrganizer\" "
if [ "${replyToOrganizer}" == "true" ] ; then
  replyToOrganizerSelection+="value=\"true\" checked=\"checked\"/> "
else
  replyToOrganizerSelection+="value=\"true\"/> "
fi
replyToOrganizerSelection+="League Organizer <i class=\"muted\">(${OrganizerEmail})</i>"

# Compute the Game Selection Drop down values
gameDaySelection=""
for day in Sun Mon Tue Wed Thu Fri Sat ; do
  if [ "${gameDay}" == "$day" ] ; then
    gameDaySelection+="<option value=\"$day\" selected>$day</option>"
  else
    gameDaySelection+="<option value=\"$day\">$day</option>"
  fi
done

# Compute emailStatus radio buttons
emailStatusSelection=""
if [ "${emailStatus}" == "enabled" ] ; then
  emailStatusSelection+="<input style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"enabled\" checked=\"checked\"/> Enabled"
  emailStatusSelection+="&nbsp;&nbsp;<input style=\"margin: 0;\"type=\"radio\" name=\"emailStatus\" value=\"disabled\" /> Disabled"
else
  emailStatusSelection+="<input style=\"margin: 0;\" style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"enabled\"/> Enabled"
  emailStatusSelection+="&nbsp;&nbsp;<input style=\"margin: 0;\" type=\"radio\" name=\"emailStatus\" value=\"disabled\"  checked=\"checked\"/> Disabled"
fi


# Start building the web page that will be displayed
htmlHeader

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|TAB_ADMIN|active|" template-header.html

cat << EOF
<table>
<tr>
<td>
<form action="leagueInfo.cgi" method="POST">
<fieldset>
<legend>League Information:</legend>
<input name="section" value="info" type="hidden">
<table  class="table table-hover table-condensed">

<!-- Organizer -->
<tr>
<td colspan="2"><b>Organizer Info</b></td>
</tr>
<tr>
<td style="text-align:right; border:0px; vertical-align:middle; margin-bottom:0px;">Name:</td>
<td style="border:0px; "><input class="input-small" name="organizer" type="text" id="organizer" value="${LeagueOrganizer}"></td>
</tr>
<tr>
<td style="text-align:right; border:0px; vertical-align:middle; margin-bottom:0px;">Email:</td>
<td style="border:0px;">
  <div class="input-prepend"><span class="add-on"><i class="icon-envelope"></i></span>
   <input type="email" class="input-xlarge" name="organizerEmail" size="35" id="organizerEmail" value="${OrganizerEmail}">
  </div>
</td>
<!-- Reply-To -->
<tr>
  <td style="text-align:right; border:0px;" title="$replyToOrganizerTitle">Reply-To:</td>
  <td style="text-align:left; border:0px;" title="$replyToOrganizerTitle">${replyToOrganizerSelection}</td>
</tr>

<!-- GMail Account Info -->
  <tr>
  <td  colspan="2"><b>Gmail Info</b></td>
  <tr>
<tr>
  <td style="text-align:right; border:0px;">Name:</td>
  <td style=" border:0px;"><input style="float:left;" name="leagueEmailName" type="text" id="leagueEmailName" value="${EmailAccountName}"></td>
</tr>

<tr>
  <td style="text-align:right; border:0px;">Address:</td>
  <td style="border:0px;">
   <div class="input-prepend"><span class="add-on"><i class="icon-envelope"></i></span>
    <input class="input-xlarge" name="leagueEmailAddress" type="email" id="leagueEmailAddress" value="${EmailAccountAddress}">
   </div>
  </td>
</tr>
<tr>
  <td style="text-align:right; border:0px">pwd:</td>
  <td style="border: 0px;">
    <div class="input-prepend"><span class="add-on"><i class="icon-key" ></i></span>
      <input class="input-small" name="leagueEmailPwd" type="password" size="10" id="leagueEmailPwd" value="${EmailAccountPass}">
    </div>
   </td>
</tr>
<!-- GAME DAY -->
<tr>
<td colspan="2"><b>Game Info</b><td>
</tr>
<tr><td style="text-align:right; border:0px;">Game Day:</td>
    <td style="border:0px;">
      <div class="input-prepend">
        <span class="add-on"><i class="icon-calendar"></i></span>
        <select name="gameDay" class="input-small">$gameDaySelection</select>
      </div>
    </td>
<tr>
    <td style="text-align:right; border:0px;">start:</td>   
    <td style="border:0px;">
      <div id="startTimePicker" class="input-prepend">
        <span class="add-on"><i class="icon-time"></i></span>
        <input  data-format="HH:mm PP" name="gameStart" type="text" class="input-mini add-on-target" id="startTimePicker" value="${gameStart}"/>
      </div>
    </td>
</tr>
<tr>
    <td style="text-align:right; border:0px;">end:</td>
    <td style="border:0px;">
      <div id="endTimePicker" class="input-prepend">
        <span class="add-on"><i class="icon-time" ></i></span>
        <input data-format="HH:mm PP" name="gameEnd" type="text" class="input-mini add-on-target" id="gameEnd" value="${gameEnd}"/>
      </div>
    </td>
</tr>
<tr>
    <td style="text-align:right; border:0px;">location:</td>
    <td style="border:0px;">
      <div class="input-prepend">
      <span class="add-on"><i class="icon-globe"></i></span>
      <input name="gameLocation" type="text" class="input-medium" value="${gameLocation}"/>
      </div>
</td>
</tr>
<tr>
  <td style="text-align:right">Max Players:</td>
  <td>
   <div class="input-prepend"><span class="add-on"><i class="icon-group"></i></span>
     <input name="maxSpots" type="number" class="input-mini" id="maxSpots" value="${maxSpots}">
   </div>
  </td>
</tr>
<tr><td style="text-align:right; border:0px;">Spare Fee: </td>
<td style="border:0px;">
 <div class="input-prepend"><span class="add-on"><b>$</b></span>
  <input name="spareFee" type="number" class="input-mini" id="spareFee" value="${spareFee}"/>
 </div>
</td>
</tr>
<tr>
<td class="input"><input type="submit" value="Update" /></td><td></td></tr>
</table>
</fieldset>
</form>
</td>
</tr>
</table>


EOF

cat template-footer.html


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
<h4>League Information</h4>

<div class="row-fluid" style="padding:0px 0px 10px 0px;">
  <div class="span5 bubble-fieldset" >
    <!-- Organizer Info -->
    <legend>Organizer Info</legend>
    <form action="leagueInfo.cgi" method="POST" class="form-inline" >
      <input name="section" value="info" type="hidden"/>
      
      <!-- Organizer Name -->
      <div>
        <label class="form-label" for="organizer">Name:</label>
        <input type="text" class="input-small" name="organizer" id="organizer" value="${LeagueOrganizer}"/>
      <div>
      
      <!-- Organizer Email -->
      <div class="btn-pad-top">
          <label class="form-label" for="organizerEmail">Email:</label>
          <div class="input-prepend"><span class="add-on"><i class="icon-envelope"></i></span>
             <input type="email" class="input-xlarge" name="organizerEmail" id="organizerEmail" value="${OrganizerEmail}"/>
          </div>
      </div>
      
      <!-- Reply-To -->
      <div class="btn-pad-top">
          <label class="form-label" for="subject" >Reply-To:</label>
          <input type="checkBox" name="replyToOrganizer" value="true" checked="checked"/>&nbsp;League Organizer <i class="muted">(${OrganizerEmail})</i>
      </div>
      <!-- update button -->
      <div class="btn-pad-top">
         <button type="submit" class="btn btn-small btn-primary" >Update</button>
      </div>
    </form>        
  </div>
</div> <!--/class="row-fluid" -->

<div class="row-fluid">
  <div class="span5 bubble-fieldset" >
  <legend >Gmail Account Info</legend>
    <form action="leagueInfo.cgi" method="POST" class="form-horizontal form-indent" >
      <!-- Gmail Account Info -->
      <input name="section" value="gmail" type="hidden">
      <!-- Gmail Name -->
      <div class="control-group">
      <label class="control-label" for="leagueEmailName">Name:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-tag"></i></span>
          <input type="text" class="input-large" name="leagueEmailName" id="leagueEmailName" value="${EmailAccountName}"/>

        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Gmail Address -->
    <div class="control-group">
      <label class="control-label" for="leagueEmailAddress">Email:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-envelope"></i></span>
          <input type="email" class="input-xlarge" name="leagueEmailAddress" id="leagueEmailAddress" value="${EmailAccountAddress}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->
   
    <!-- Gmail Address -->
    <div class="control-group">
      <label class="control-label" for="leagueEmailPwd">Password:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-key"></i></span>
          <input type="password" class="input-large" name="leagueEmailPwd" id="leagueEmailPwd" value="${EmailAccountPass}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

        <!-- update button -->
        <div class="control-group">
          <div class="controls">
           <button type="submit" class="btn btn-small btn-primary" >Update</button>
           
          </div>
        </div>
  
</form>

</div>
</div>

EOF

cat template-footer.html


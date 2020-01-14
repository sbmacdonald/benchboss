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

# Compute the Game Selection Drop down values
gameDaySelection=""
for day in Sun Mon Tue Wed Thu Fri Sat ; do
  if [ "${gameDay}" == "$day" ] ; then
    gameDaySelection+="<option value=\"$day\" selected>$day</option>"
  else
    gameDaySelection+="<option value=\"$day\">$day</option>"
  fi
done


# Start building the web page that will be displayed
htmlHeader

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|TAB_ADMIN|active|" template-header.html

cat << EOF
<div class="row-fluid" style="padding:15px 0px 10px 0px;">
<div class="span5 bubble-fieldset" >
<legend>Game Information</legend>
<form action="schedule.html" method="POST" class="form-horizontal">
  <input name="section" value="info" type="hidden">

  <!-- Game Info -->

    <!-- Game Day -->
    <div class="control-group">
      <label class="control-label" for="gameDay">Game Day:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-calendar"></i></span>
          <select name="gameDay" class="input-small">$gameDaySelection</select>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Game Start -->
    <div class="control-group">
      <label class="control-label" for="startTime">Start Time:</label>
      <div class="controls">
        <div id="startTimePicker" class="input-prepend">
          <span class="add-on"><i class="icon-time"></i></span>
          <input readonly style="background-color: #ffffff;cursor: pointer;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="gameStart" id="startTime" value="${gameStart:-9:00 PM}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Game End -->
    <div class="control-group">
      <label class="control-label" for="gameEnd">End Time:</label>
      <div class="controls">
        <div id="endTimePicker" class="input-prepend">
          <span class="add-on"><i class="icon-time" ></i></span>
          <input readonly style="background-color: #ffffff;cursor: pointer;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="gameEnd" id="gameEnd" value="${gameEnd:-10:00 PM}"/>
          </div>
      </div>
    </div>
    
    <!-- Location -->
    <div class="control-group">
      <label class="control-label" for="gameLocation">Location:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-globe"></i></span>
          <input type="text" class="input-medium" name="gameLocation" id="gameLocation" value="${gameLocation}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Max Players -->
    <div class="control-group">
      <label class="control-label" for="maxSpots">Max Players:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><i class="icon-group"></i></span>
          <input type="number" class="input-mini" name="maxSpots" id="maxSpots" value="${maxSpots:-20}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->
   
    <!-- Spare Fee -->
    <div class="control-group">
      <label class="control-label" for="spareFee">Spares Fee:</label>
      <div class="controls">
        <div class="input-prepend"><span class="add-on"><b>$</b></span>
          <input type="number" class="input-mini" name="spareFee" id="spareFee" value="${spareFee:-10}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <div class="control-group">
      <div class="controls">
        <button type="submit" class="btn btn-small btn-primary">Update</button>
      </div>
    </div>
     
</form>
</div>
</div>

EOF

cat template-footer.html


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

# Some LeagueTypes don't have goalies, so we hide the
# goalie admin menu item
case ${LeagueType} in
  Hockey|Soccer)admin_goalie="display:"; ;;
  *)admin_goalie="display:none"; ;;
esac

# update variables
sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
    -e "s|USERNAME|$REMOTE_USER|g" \
    -e "s|ADMIN_GOALIES|${admin_goalies}|g" \
    -e "s|TAB_ADMIN|active|" template-header.html

cat << EOF
<h4>&nbsp;</h4>

<div class="row-fluid" style="padding:0px 0px 10px 0px;">
<div class="span5 bubble-fieldset" >
  <legend>Game Information</legend>
  <form action="schedule.html" method="POST" class="form-horizontal form-indent">
      <input name="section" value="info" type="hidden">

    <!-- Game Day -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="gameDay">Game Day:</label>
      <div class="controls" style="margin-left:auto;">
        <div class="input-prepend"><span class="add-on"><i class="icon-calendar"></i></span>
          <select name="gameDay" class="input-small">$gameDaySelection</select>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Game Start -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="startTime">Start Time:</label>
      <div class="controls inline" style="margin-left:auto">
        <div id="startTimePicker" class="input-prepend">
          <span class="add-on"><i class="icon-time"></i></span>
          <input readonly style="background-color: #ffffff;cursor: pointer; ; width: 60px;" type="text" data-format="HH:mm PP" class="input-mini add-on-target" name="gameStart" id="startTime" value="${gameStart:-9:00 PM}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Game End -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="gameEnd">End Time:</label>
      <div class="controls" style="margin-left:auto">
        <div id="endTimePicker" class="input-prepend">
          <span class="add-on"><i class="icon-time" ></i></span>
          <input readonly class="input-mini add-on-target" style="background-color: #ffffff;cursor: pointer; width: 60px;" type="text" data-format="HH:mm PP"  name="gameEnd" id="gameEnd" value="${gameEnd:-10:00 PM}"/>
          </div>
      </div>
    </div>
    
    <!-- Location -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="gameLocation">Location:</label>
      <div class="controls" style="margin-left:auto">
        <div class="input-prepend"><span class="add-on"><i class="icon-globe"></i></span>
          <input type="text" class="input-medium" style="width: 100px"; name="gameLocation" id="gameLocation" value="${gameLocation}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <!-- Max Players -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="maxSpots">Max Players:</label>
      <div class="controls" style="margin-left:auto">
        <div class="input-prepend"><span class="add-on"><i class="icon-group"></i></span>
          <input type="number" class="input-mini" style="width: 40px;" name="maxSpots" id="maxSpots" value="${maxSpots}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->
   
    <!-- Spare Fee -->
    <div class="control-group">
      <label class="control-label" style="width:auto;margin-right:5px; float: left;" for="spareFee">Spares Fee:</label>
      <div class="controls" style="margin-left:auto">
        <div class="input-prepend"><span class="add-on"><b>$</b></span>
          <input type="number" class="input-mini" style="width: 40px;" name="spareFee" id="spareFee" value="${spareFee}"/>
        </div>
      </div> <!-- /controls -->
    </div> <!-- /control-group -->

    <div class="control-group">
      <div class="controls">
        <button type="submit" class="btn btn-small btn-primary">Update</button>
      </div>
    </div>    

</div> <!--/class="row-fluid" -->
 
</form>
</div>
</div>

EOF

cat template-footer.html


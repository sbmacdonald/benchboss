#!/bin/bash
#
#

. functions
. admin.func

cgiVars
. ${DATA_DIR}/league.cfg

chmod -f 777 $LEAGUE_CFG

LOG_FILE="$(getLogFile $BASH_SOURCE)"

# Depending on the section being upated, assume all values have changed and
# update them
if [ ! -z ${CGI_section} ] ; then
  chmod 777 $leagueLogFile
  case "$CGI_section" in
    info)
      #infoKeys=(gameDay gameStart gameEnd gameLocation emailStatus spareFee maxSkaters)
      #for ((i=0; i < ${#infoKeys[@]}; i++)) ; do 
      #  getConfigValue ${infoKeys[$i]} "`eval echo \\\$CGI_${infoKeys[$i]}`" val newVal
      #  if [ $? -eq 1 ] ; then 
      #    key=${infoKeys[$i]}
      #    logInfo "Key '${key}' updated from: '$val' to: '$newVal'" 
      #    sed -i "s|^${key}.*|${key}=\"$newVal\"|g" $LEAGUE_CFG
      #  fi 
      #done
      logInfo "[$REMOTE_USER]: Updating League Info From: LeagueName: ${EmailAccountName} MaxSkaters:${maxSkaters} DenyRegs:${denyRegulars} MaxGoalies:${maxGoalies} SparesFee:${sparesFee} BeerTracker:${beerTracker} ScoreTracker:${scoreTracker} AdminName:${LeagueOrganizer}  AdminEmail:${OrganizerEmail} notifyRecinded:${notifyRecinded}" >> $leagueLogFile
      sed -i "s|^EmailAccountName.*|EmailAccountName=\"${CGI_leagueEmailName}\"|g" ${LEAGUE_CFG}
      sed -i "s|^maxSkaters.*|maxSkaters=${CGI_maxSkaters}|g" ${LEAGUE_CFG}
      sed -i "s|^denyRegulars.*|denyRegulars=\"${CGI_denyRegulars}\"|g" ${LEAGUE_CFG}
      sed -i "s|^maxGoalies.*|maxGoalies=${CGI_maxGoalies}|g" ${LEAGUE_CFG}
      sed -i "s|^spareFee.*|spareFee=${CGI_spareFee}|g" ${LEAGUE_CFG}
      sed -i "s|^beerTracker.*|beerTracker=\"${CGI_beerTracker}\"|g" ${LEAGUE_CFG}
      if [ "${CGI_beerTracker}" == "yes" ] ; then
        setupBeerTracker
      fi
      sed -i "s|^scoreTracker.*|scoreTracker=\"${CGI_scoreTracker}\"|g" ${LEAGUE_CFG}
      
      sed -i "s|^LeagueOrganizer.*|LeagueOrganizer=\"${CGI_organizer}\"|g" ${LEAGUE_CFG}
      sed -i "s|^OrganizerEmail.*|OrganizerEmail=\"${CGI_organizerEmail}\"|g" ${LEAGUE_CFG}
      sed -i "s|^notifyRecinded.*|notifyRecinded=\"${CGI_notifyRecinded}\"|g" ${LEAGUE_CFG}
      logInfo "[$REMOTE_USER]: Updated  League Info   To: LeagueName: ${CGI_leagueEmailName} MaxSkaters:${CGI_maxSkaters} DenyRegs:${CGI_denyRegulars} MaxGoalies:${CGI_maxGoalies} SparesFee:${CGI_sparesFee} BeerTracker:${CGI_beerTracker} ScoreTracker:${CGI_scoreTracker} AdminName:${CGI_organizer}  AdminEmail:${CGI_organizerEmail} notifyRecinded:${CGI_notifyRecinded}" >> $leagueLogFile
    ;;

  esac
fi

# Pick up the new values
. $LEAGUE_CFG

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
    -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
    -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
    -e "s|ADMIN_GOALIES|${admin_goalies}|g" \
    -e "s|TAB_ADMIN|active|" template-header.html

# Compute denyRegulars options
denyRegularsOptions=""
if [ "${denyRegulars}" == "no" ] ; then
  denyRegularsOptions="<option value=\"yes\">yes</option><option value=\"no\" selected>no</opt#ion>"
else
  denyRegularsOptions="<option value=\"yes\" selected>yes</option><option value=\"no\">no</option>"
fi

beerTrackerOptions=""
if [ "${beerTracker}" == "no" ] ; then
  beerTrackerOptions="<option value=\"yes\">yes</option><option value=\"no\" selected>no</option>"
else
  beerTrackerOptions="<option value=\"yes\" selected>yes</option><option value=\"no\">no</option>"
fi

scoreTrackerOptions=""
if [ "${scoreTracker}" == "no" ] ; then
  scoreTrackerOptions="<option value=\"yes\">yes</option><option value=\"no\" selected>no</option>"
else
  scoreTrackerOptions="<option value=\"yes\" selected>yes</option><option value=\"no\">no</option>"
fi

notifyRecindedOptions=""
if [ "${notifyRecinded}" == "no" ] ; then
  notifyRecindedOptions="<option value=\"yes\">yes</option><option value=\"no\" selected>no</option>"
else
  notifyRecindedOptions="<option value=\"yes\" selected>yes</option><option value=\"no\">no</option>"
fi

case ${LeagueType} in
  Hockey)player_label="Skaters";
         goalie_display="display:"
         ;;
  Soccer)player_label="Players";
         goalie_display="display:";
         ;;
  *)player_lable="Players";
    goalie_display="display:none"
    ;;
esac
case ${LeagueType}
cat << EOF
<div class="row-fluid" style="padding:15px 0px 10px 0px;">
<div class="span5 bubble-fieldset" >
<legend>League Information</legend>
<form action="leagueInfoVariable.html" method="POST" class="form-horizontal">
  <input name="section" value="info" type="hidden">
  
  <!-- League Name -->
  <div class="control-group">
    <label class="control-label" style="width:auto; margin-right:8px" for="leagueEmailName">League Name:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on"><i class="icon-tag"></i></span>
        <input type="text" class="input-large" name="leagueEmailName" id="leagueEmailName" value="${EmailAccountName}"/>
        <a href="#leagueNameModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>        
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Max Skaters -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:18px" for="maxSkaters">Max ${player_label}:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on"><i class="icon-group"></i></span>
        <input type="number" class="input-mini" name="maxSkaters" id="maxSkaters" value="${maxSkaters:-20}"/>
        <div class="input-append">
          <a href="#maxSkatersModal" role="button" data-toggle="modal">
            <span class="add-on" style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
          </a>
        </div>
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Deny Regulars -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:3px" for="denyRegulars">Deny Regulars:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on"><i class="icon-ban-circle"></i></span>
        <select class="input-mini" name="denyRegulars" id="denyRegulars">${denyRegularsOptions}</select>
        <a href="#denyRegularsModal" role="button" data-toggle="modal">
          <span class="add-on" style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>
      </div> 
    </div> <!-- /controls -->
 </div> <!-- /control-group -->


   <!-- Max Goalies -->
  <div class="control-group" style="${goalie_display}">
    <label class="control-label" style="width:auto;margin-right:18px" for="maxGoalies">Max Goalies:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on"><i class="icon-group"></i></span>
        <input type="number" class="input-mini" name="maxGoalies" id="maxGoalies" value="${maxGoalies:-2}"/>
        <div class="input-append">
          <a href="#maxGoaliesModal" role="button" data-toggle="modal">
            <span class="add-on" style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
          </a>
        </div>

      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->
    
  <!-- Spare Fee -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:23px" for="spareFee">Spares Fee:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on"><b>$</b></span>
        <input type="number" class="input-mini" name="spareFee" id="spareFee" value="${spareFee:-10}"/>
        <a href="#sparesFeeModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Beer Tracker -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:14px" for="spareFee">Beer Tracker:</label>
    <div class="controls" style="margin-left:auto;">
      <!--<div class="input-prepend"><span class="add-on icon-briefcase"></span>-->
       <div class="input-prepend"><span class="add-on"><img src="../../Common/bootstrap/img/glyphicons_274_beer.png" style="width:14px;height=16px;"/></span>
        <select class="input-mini" id="beerTracker" name="beerTracker">${beerTrackerOptions}</select>
        <a href="#beerTrackerModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>        
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Score Tracker -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:14px" for="scoreTracker">Score Tracker:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on icon-bar-chart"></span>
        <select class="input-mini" id="scoreTracker" name="scoreTracker">${scoreTrackerOptions}</select>
        <a href="#scoreTrackerModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>        
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Organizer Name -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:13px" for="organizer">Admin Name:</label>
    <div class="controls" style="margin-left:auto;">
      <div class="input-prepend"><span class="add-on icon-user"></span>
      <input type="text" class="input-small" name="organizer" id="organizer" value="${LeagueOrganizer}"/>
        <a href="#adminNameModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Organizer Email -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:15px;" for="organizerEmail">Admin Email:</label>
    <div class="controls" style="margin-left:auto">
      <div class="input-prepend"><span class="add-on"><i class="icon-envelope"></i></span>
        <input type="email" class="input-large" name="organizerEmail" id="organizerEmail" value="${OrganizerEmail}"/>
        <a href="#adminEmailModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>
      </div>
    </div> <!-- /controls -->
  </div> <!-- /control-group -->

  <!-- Recinded Email -->
  <div class="control-group">
    <label class="control-label" style="width:auto;margin-right:15px;" for="playerRecindedNotify">Dropout Notify:</label>
    <div class="controls" style="margin-left:auto">
      <div class="input-prepend"><span class="add-on"><i class="icon-flag"></i></span>
        <select class="input-mini" id="notifyRecinded" name="notifyRecinded">${notifyRecindedOptions}</select>
        <a href="#notifyRecindedModal" role="button" data-toggle="modal">
          <span class="add-on"  style="border:none; background-color: #F2EFE9;"><i class="icon-question-sign"></i></span>
        </a>
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

<!-- Example Modal -->
<div id="myModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Modal header</h3>
  </div>
  <div class="modal-body">
    <p>One fine body…</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
    <button class="btn btn-primary">Save changes</button>
  </div>
</div> <!-- Example Modal -->

<!-- League Name Modal -->
<div id="leagueNameModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">League Name</h3>
  </div>
  <div class="modal-body">
    <p>This name will appear as the "From:" name in the RSVP emails.</p>
    <img src="../../Common/img/bb_inbox.png" class="img-polaroid"/>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- league Name Modal -->

<!-- Max Skaters Modal -->
<div id="maxSkatersModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Max Skaters</h3>
  </div>
  <div class="modal-body">
    <p>The maximum number of skaters allowed per game.</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Max Skaters Modal -->

<!-- Deny Regulars Modal -->
<div id="denyRegularsModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Deny Regulars</h3>
  </div>
  <div class="modal-body">
    <p>If a regular replies after the roster has been filled (by spares) should the regular be allowed to come or should they be denied for responding too slowly ?</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Deny Regulars Modal -->

<!-- Max Goalies Modal -->
<div id="maxGoaliesModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Max Goalies</h3>
  </div>
  <div class="modal-body">
    <p>How many goalies do you need at the game ?</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Max Skaters Modal -->


<!-- Spares Fee Modal -->
<div id="sparesFeeModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Spares Fee</h3>
  </div>
  <div class="modal-body">
    <p>When spares click the 
<span style="display:inline-block;"><!--[if mso]>
  <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="URL_BASE/rsvp.cgi?email=PLAYER_EMAIL&action=in" style="height:26px;v-text-anchor:middle;width:130px;" arcsize="20%" stroke="f" fillcolor="#658208">
    <w:anchorlock/>
    <center>
    <![endif]-->
    <a href="#" style="background-color:#658208;border-radius:5px;color:#ffffff;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:26px;text-align:center;text-decoration:none;width:130px;-webkit-text-size-adjust:none;">I'd like to come !</a>
    <!--[if mso]>
    </center>
    </v:roundrect>
    <![endif]--></span> button they are reminded to bring the $ spares fee:
    <p><img src="../../Common/img/bb_spare-in-message.png" class="img-polaroid"/></p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- SparesFee Modal -->


<!-- Beer Tracker Modal -->
<div id="beerTrackerModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Beer Tracker</h3>
  </div>
  <div class="modal-body">
    <p>Does your group have beer after the game ? </p>
    <p>Do you share beer duty ? </p>
    <p>If so you may find the "Beer Tracker" helpful: </p>
    <p>An additional 
<span style="display:inline-block;"><!--[if mso]>
  <v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="#" style="height:26px;v-text-anchor:middle;width:130px;" arcsize="20%" stroke="f" fillcolor="#FBB117">
  <w:anchorlock/>
  <center>
<![endif]-->
<a href="#" style="background-color:#FBB117;border-radius:5px;color:#ffffff;display:inline-block;font-family:sans-serif;font-size:13px;font-weight:bold;line-height:26px;text-align:center;text-decoration:none;width:130px;-webkit-text-size-adjust:none;">I'll bring beer</a>
<!--[if mso]>
  </center>
  </v:roundrect>
<![endif]--></span> button will be included in the RSVP emails that allows regulars to sign-up for bringing beer for the game.  Once a player has brought beer, they will not get the button until everyone else has taken a turn being the "beer guy".</p>
  <p>The attendance page will indicate who has volunteered tro bring beer:</p>
  <img src="../../Common/img/BB_att_with_beer_duty.png" class="img-polaroid"/>  
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Beer Tracker Modal -->

<!-- Score Tracker Modal -->
<div id="scoreTrackerModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Score Tracker</h3>
  </div>
  <div class="modal-body">
    <p>Each game in the schedule will have an Opponent field, and fields for the Scores</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Score Tracker Modal -->

<!-- Admin Name Modal -->
<div id="adminNameModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Admin Name</h3>
  </div>
  <div class="modal-body">
    <p>Your name, which is used as the signature of the emails.</p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Adminm Name Modal -->


<!-- Admin Email Modal -->
<div id="adminEmailModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Admin Email</h3>
  </div>
  <div class="modal-body">
    <p>Your personal email address. </p>
    <p>If a player replies to one of the RSVP/Invite emails, the reply will be forwarded to this address so you are kept in the loop. </p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Adminm Email Modal -->

<!-- Notify Recinded Modal -->
<div id="notifyRecindedModal" class="modal hide" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
  <div class="modal-header">
    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">×</button>
    <h3 id="myModalLabel">Dropout Notify</h3>
  </div>
  <div class="modal-body">
    <p>Send me a "Dropout Notification" email when someone drops out of game. </p>
  </div>
  <div class="modal-footer">
    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
  </div>
</div> <!-- Adminm Email Modal -->


EOF

cat template-footer.html


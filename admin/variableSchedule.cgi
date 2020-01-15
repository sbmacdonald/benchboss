#!/bin/bash
. functions
. variableSchedule.func

cgiVars
. ${DATA_DIR}/league.cfg

secondsPerWeek=604800
chmod 777 ${SCHEDULE}

# date math
#date -d "Nov 19 + 10 weeks" +%s
#date -d "19/11/2013 + 10 weeks" +%s
#
#for i in `seq 1 10` ; do date -d"today + $i days" +"%a %b %d %Y"; done
#Sun Nov 10 2013
#Mon Nov 11 2013
#Tue Nov 12 2013
#Wed Nov 13 2013
#Thu Nov 14 2013
#Fri Nov 15 2013
#Sat Nov 16 2013
#Sun Nov 17 2013
#Mon Nov 18 2013
#Tue Nov 19 2013
#
# Compute number of hours between (this time) tomorrow and now
# echo "$(( $(( $(date -d"today + 1 day" +%s) - $(date +%s))) / 3600))"
#
# Compute number of weeks between two dates:
# echo "$(( $(( $(date -d"today + 10 weeks" +%s) - $(date +%s))) / 604800))"
#
#secondsPerWeek=604800
#echo "$(( $(( $(date -d"01/18/2014" +%s) - $(date -d"11/09/2013" +%s))) / ${secondsPerWeek} ))"
#
# start=11/09/2013
# end=01/18/2014
# echo "$(( $(( $(date -d"${end}" +%s) - $(date -d"${start}" +%s))) / ${secondsPerWeek} ))"

case ${LeagueType} in
  Hockey|Soccer)admin_goalies="display:"; ;;
  *)admin_goalies="display:none"; ;;
esac

chmod -f 777 /tmp/variableSchedule.log
echo "CGI_action: ${CGI_action} CGI_glist: ${CGI_glist}" >> /tmp/variableSchedule.log
# Check if there was an action specified, otherwise just display the page
if [[ "$CGI_action" == "" ]] || [ "$CGI_s" == "rns" ] ; then
  htmlHeader

  sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
      -e "s|USERNAME|$REMOTE_USER|g" \
      -e "s|SUPERUSER_ADMIN_PAGE|${BB_ADMIN_LINK}|" \
      -e "s|BEER_MENU_DISPLAY|$([ \"$beerTracker\" == \"yes\" ] && echo yes || echo none)|" \
      -e "s|ADMIN_GOALIES|${admin_goalies}|" \
      -e "s|TAB_ADMIN|active|" template-header.html

  if [ "$CGI_s" == "rns" ] ; then
    echo "<h4 style=\"color:red\">Registration email not sent (emailStatus == disabled)</h4>"
  fi
  printVariableSchedulePage

  cat template-footer.html

else

  # An action was specified... handle it !  
  case "$CGI_action" in
    mtd)
      deleteGames
      ;;
    mtc)
      cancelGames
      ;;
    mta)
      reinstateGames
      ;;
    update)
      date >> /tmp/addGame.cgi.input
      echo "variableSchedule.cgi::$CGI_action CGI_action: $CGI_action" >> /tmp/addGame.cgi.input
      echo "variableSchedule.cgi::$CGI_action CGI_gameId: $CGI_gameId" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_dpd1: $CGI_dpd1" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_location: $CGI_location" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_gameStart: $CGI_gameStart" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_gameEnd: $CGI_gameEnd" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_dpd2: $CGI_dpd2" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origGameTimestamp: $CGI_origGameTimestamp" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origGameDay: $CGI_origGameDay" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origGameStart: $CGI_origGameStart" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origLocation: $CGI_origLocation" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origGameEnd: $CGI_origGameEnd" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi::$CGI_action CGI_origActive: $CGI_origActive" >> /tmp/addGame.cgi.input
      
      # Prevent unsafe modifications (empty fields)
      if [[ "$CGI_dpd1" != "" &&  "$CGI_location" != "" && "$CGI_gameStart" != "" \
         && "$CGI_gameEnd" != "" && "CGI_origGameStart" != "" \
         && "$CGI_origLocation" != "" && "$CGI_origGameEnd" != "" ]] ; then
        
        updatedGameDay=${CGI_dpd1}
        updatedGameStart=${CGI_gameStart}
        updatedGameEnd=${CGI_gameEnd}
        updatedGameTimestamp=$(date -d"${CGI_dpd1} 0:00" +%s)
        sed -i "s|^${CGI_gameId}~.*|${CGI_gameId}~${updatedGameTimestamp}~${updatedGameDay}~${updatedGameStart}~${CGI_location}~${updatedGameEnd}~${CGI_origActive}~${CGI_opponent}~${origPtsFor}~${origPtsAgainst}|" ${SCHEDULE}
        logInfo "Update Game($REMOTE_USER) from: ${gameId}~${CGI_origGameTimestamp}~${CGI_origGameDay}~${CGI_origGameStart}~${CGI_origLocation}~${CGI_origGameEnd}~${CGI_origActive}~${CGI_origOpponent}~${origPtsFor}~${origPtsAgainst}" >> $scheduleLogFile
        logInfo "Update Game($REMOTE_USER)   to: ${gameId}~${updatedGameTimestamp}~${updatedGameDay}~${updatedGameStart}~${CGI_location}~${updatedGameEnd}~${CGI_origActive}~${CGI_opponent}~${origPtsFor}~${origPtsAgainst}" >> $scheduleLogFile
      else
        logWarning "Update GAME($REMOTE_USER) from: Failed: Unsafe: $CGI_dpd1~$CGI_location~$CGI_dpd2" >> $scheduleLogFile
      fi
      ;;
    score)
      updatedPtsFor=${CGI_ptsFor}
      updatedPtsAgainst=${CGI_ptsAgainst}
      # sample schedule:
      # b1ef0c07dfa190bda264566454188e6b~1411444800~09/23/2014~8:30 PM~Metro Center~9:30 PM~p~???~7~6
      #85cc720273e6a23f765f3a7654188e6b~1412654400~10/07/2014~9:30 PM~Metro Center~10:30 PM~p~EY/PWC~~
      #        gameId~date~Date~startTime~Location~Endtime~Status~Opponent~ptsFor~ptsAgainst
      #          \1   \2    \3     \4       \5       \6      \7     \8
      sed -i "s|^\(${CGI_gameId}\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)~\(.*\)|\1~\2~\3~\4~\5~\6~\7~\8~${updatedPtsFor}~${updatedPtsAgainst}|" ${SCHEDULE}
      #sed -i "s|^${CGI_gameId}~.*|${CGI_gameId}~${updatedGameTimestamp}~${updatedGameDay}~${updatedGameStart}~${CGI_location}~${updatedGameEnd}~${CGI_origActive}~${updatedOpponent}~${updatedPtsFor}~${updatedPtsAgainst}|" ${SCHEDULE}
      logInfo "Game Score($REMOTE_USER) from: ${gameId} ${LEAGUE_ACRO}: ${CGI_origPtsFor} ${CGI_origOpponent}: ${CGI_origPtsAgainst}" >> $scheduleLogFile
      logInfo "Game Score($REMOTE_USER)   to: ${gameId} ${LEAGUE_ACRO}: ${updatedPtsFor} ${updatedOpponent}: ${updatedPtsAgainst}" >> $scheduleLogFile
      ;;
    add)
      #echo "variableSchedule.cgi: CGI_action: $CGI_action" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi: CGI_dpd1: $CGI_dpd1" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi: CGI_location: $CGI_location" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi: CGI_gameStart: $CGI_gameStart" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi: CGI_gameEnd: $CGI_gameEnd" >> /tmp/addGame.cgi.input
      #echo "variableSchedule.cgi: CGI_dpd2: $CGI_dpd2" >> /tmp/addGame.cgi.input
      
      # Prevent Incomplete games
      if [[ "$CGI_dpd1" != "" &&  "$CGI_location" != "" && "$CGI_gameStart" != "" \
         && "$CGI_gameEnd" != "" &&  "$CGI_dpd2" != "" ]] ; then

        # see if there are multiple games being added
        secondsPerWeek=604800
        ##startWeek=$(date -d"$(date -d"${CGI_dpd1}" +%m/%d/%Y) 0:00" +%s)
        ##endWeek=$(date -d"$(date -d@${CGI_dpd2} +%m/%d/%Y) 0:00" +%s)

        #startWeek=$(date -d"${CGI_dpd1} ${CGI_gameStart}" +%s)
        #endWeek=$(date -d"${CGI_dpd2} ${CGI_gameStart}" +%s)
        #weeks=$(($((${endWeek} - ${startWeek})) / ${secondsPerWeek}))
        startWeek=$(date -d"${CGI_dpd1} 0:00" +%s)
        endWeek=$(date -d"${CGI_dpd2} 0:00" +%s)
        #weeks=$(($((${endWeek} - ${startWeek})) / ${secondsPerWeek}))
        weeks=`awk -vend=$endWeek -vstart=$startWeek 'BEGIN{printf "%.0f",(end-start)/604800}'`
        for ((w=0; w <= ${weeks}; ++w)) ; do
          #nextGameDay=$(date -d"$(date -d"${CGI_dpd1} 0:00") + $w weeks" +%m/%d/%Y)
          #nextGameStart=$(date -d"$(date -d"${CGI_dpd1} ${CGI_gameStart}") + $w weeks" +%s)
          #nextGameEnd=$(date -d"$(date -d"${CGI_dpd1} ${CGI_gameEnd}") + $w weeks" +%s)
          gameId=`dbus-uuidgen`
          nextGameTimestamp=$(date -d"${CGI_dpd1} + $w weeks" +%s)
          nextGameDay=$(date -d"${CGI_dpd1} + $w weeks" +%m/%d/%Y)
          nextGameStart=${CGI_gameStart}
          nextGameEnd=${CGI_gameEnd}
          if [[ ${scoreTracker} == "yes" ]] ; then
            nextGameOpponent=${CGI_opponent}
          fi
          # Prevent Duplicates !
          grep -q ".*~${nextGameDay}~${nextGameStart}~.*~.*" ${SCHEDULE}
          if [ $? -ne 0 ] ; then
            if [[ ${scoreTracker} == "yes" ]] ; then
              logInfo "Add Game($REMOTE_USER): adding: ${nextGameStart}~${CGI_location}~${nextGameEnd}~u~${nextGameOpponent}~~" >> $scheduleLogFile
              echo "${gameId}~${nextGameTimestamp}~${nextGameDay}~${nextGameStart}~${CGI_location}~${nextGameEnd}~u~${nextGameOpponent}~~" >> ${SCHEDULE}
              sort -t~ -k2,2 -n ${SCHEDULE} -o ${SCHEDULE}
            else
              logInfo "Add Game($REMOTE_USER): adding: ${nextGameStart}~${CGI_location}~${nextGameEnd}" >> $scheduleLogFile
              echo "${gameId}~${nextGameTimestamp}~${nextGameDay}~${nextGameStart}~${CGI_location}~${nextGameEnd}~u~~~" >> ${SCHEDULE}
              sort -t~ -k2,2 -n ${SCHEDULE} -o ${SCHEDULE}
            fi
          else
            logInfo "Add GAME($REMOTE_USER) skipping duplicate: ${nextGameDay}~${nextGameStart}" >> $scheduleLogFile
          fi
        done          
      else
        logWarning "Add GAME($REMOTE_USER): Failed: Unsafe: $CGI_dpd1~$CGI_location~$CGI_dpd2" >> $scheduleLogFile
      fi
      ;;
  esac
cat << EOF
Status: 302 redirect
Location: variableSchedule.html${state}

EOF
exit
fi
  

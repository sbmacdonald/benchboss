#!/bin/bash
. functions
cgiVars
. ${DATA_DIR}/league.cfg

echo "$REMOTE_USER" >> /tmp/remote_user
chmod 777 /tmp/remote_user



# Check if there was an action specified, otherwise just display the page
if [[ "$CGI_action" == "" ]] ; then
  htmlHeader

  sed -e "s|LEAGUE_ACRO|${LEAGUE_ACRO}|g" \
      -e "s|USERNAME|$REMOTE_USER|g" \
      -e "s|TAB_ROSTER|active|" template-header.html

  printRosterPage

  cat template-footer.html

else

  # An action was specified... handle it !
  if [[ "$CGI_pos" == "goalie" ]] || [[ "$CGI_pos" == "g" ]] ; then
    pos="g"
  else
    pos="s"
  fi
  if [[ "$CGI_type" == "regular" ]] || [[ "$CGI_type" == "r" ]]; then
    type="r"
  else
    type="s"
  fi

  case "$CGI_action" in
    delete)
      if [[ $(trim $CGI_email) != "" ]] ; then
        playerRecord=`grep $email ${ROSTER}`
        logInfo "Delete($REMOTE_USER): $playerRecord" >> $rosterLogFile
        sed -i "/^${CGI_email/ /}~.*/d" ${ROSTER}
        sed -i "/^${CGI_email/ /}~.*/d" `getFilename in`
        sed -i "/^${CGI_email/ /}~.*/d" `getFilename out`
      else
        logWarning "Delete(admin): attempted to delete player with empty email address" >> $rosterLogFile
      fi
      cat << EOF
Status: 302 redirect
Location: roster.cgi

EOF
exit
      ;;
    removeMe)
      if [[ $(trim $CGI_email) != "" ]] ; then 
        playerRecord=`grep $email ${ROSTER}`
        logInfo "Delete($self): $playerRecord"" >> $rosterLogFile
      fi
      cat <<EOF
Status: 302 redirect
Location: removeMe.html

EOF
exit
      ;;
    update)
      # Prevent unsafe modifications (empty fields)
      if [[ $(trim $CGI_newemail) != "" &&  $(trim $CGI_fname) != "" && $(trim $CGI_lname) != "" ]] ; then
        sed -i "s|^$(trim $CGI_email)~.*|$(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos|" ${ROSTER}
        sed -i 's|skater|s|g' ${ROSTER}
        sed -i 's|spare|s|g' ${ROSTER}
        sed -i 's|regular|r|g' ${ROSTER}
        logInfo "Update($REMOTE_USER): $(trim $CGI_email): $(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos" >> $rosterLogFile	
        # Send the registration email iff the email changed
	if [[ $(trim $CGI_newemail) != $(trim $CGI_email) ]] ; then
          # the email address has changed, reset the confirmed flag and update any attendance files
          sed -i "s|^$(trim $CGI_email)~\(.*\)\(~[u|c]$\)|$(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos~u|" ${ROSTER}
          sed -i "s|$(trim $CGI_email)|$(trim $CGI_newemail)|" `getFilename in`
          sed -i "s|$(trim $CGI_email)|$(trim $CGI_newemail)|" `getFilename out`
          fullFile=`getFilename full`
          if [ -e "$fullFile" ] ; then
            sed -i "s|$(trim $CGI_email)|$(trim $CGI_newemail)|" $fullFile
          fi
	  sendRegistrationEmail $(trim $CGI_newemail)
	fi
      else
        logWarning "Update: Unsafe update aborted: $(trim $CGI_email): $(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos" >> $rosterLogFile
      fi
cat << EOF
Status: 302 redirect
Location: roster.cgi

EOF
exit
      ;;
    add)
      echo "roster.cgi: CGI_action: $CGI_action" >> /tmp/addPlayer.cgi.input
      echo "roster.cgi: CGI_newemail: $CGI_newemail" >> /tmp/addPlayer.cgi.input
      echo "roster.cgi: CGI_fname: $CGI_fname" >> /tmp/addPlayer.cgi.input
      echo "roster.cgi: CGI_lname: $CGI_lname" >> /tmp/addPlayer.cgi.input

      # SQLite3:
      #replace into events (id, type, location, start, end) values ( 10, 1, 'here', '8:30 pm', '10:30 pm');
      #replace into players (id, fname, lname, type, position, status) values ( 10, 'Joe', 'Smith', 1, 1, 1);
      #
      # smacdonald@mist:~$ lastName="Chris"
      # smacdonald@mist:~$ lastName="O'Brien"
      # smacdonald@mist:~$ lastName=${lastName/\'/\'\'}
      # smacdonald@mist:~$ sqlite3 LHL.db "replace into player (id, fname, lname, type, position, status) values ( 10, '$firstName', '$lastName', 1, 1, 1);"
      # smacdonald@mist:~$ sqlite3 LHL.db "select * from events;"

      #sqlite3 LHL.db "replace into player (id, fname, lname, type, position, status) values ( 11, '$fname', '$lname', 1, 1, 1);"
      
      # trim leading and trailing whitespace
      fname="$(trimWS "$CGI_fname")"
      lname="$(trimWS "$CGI_lame")"
      # handle last names like "O'Brien" and exscape them for sqlite: 'O'Brien' becomes 'O''Brien'
      lname="${lastName/\'/\'\'}"
     
      # email address should already be validated, but to be sure we'll strip all whitespace
      email=$(stripWS $CGI_newemail})
      sqlite3 LHL.db "replace into player values ( ${CGI_id}, '$fname', '$lname', $CGI_type, $CGI_pos, $CGI_status );"
      # Prevent Incomplete players, or players with unsafe email addresses
      if [[ $(trim $CGI_newemail) != "" &&  $(trim $CGI_fname) != "" && $(trim $CGI_lname) != "" ]] ; then
        # Prevent Duplicates !
        # Make sure this player (email) isn't already on the roster
        
        # strip leading and trailing spaces        
        if [ `grep -c "^$(trim $CGI_newemail)" ${ROSTER}` -eq 0 ] ; then 
          chmod 755 ${ROSTER}
          echo "$(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos" >> ${ROSTER}
          sed -i 's|skater|s|g' ${ROSTER}
          sed -i 's|spare|s|g' ${ROSTER}
          sed -i 's|regular|r|g' ${ROSTER}
          chmod 777 ${ROSTER}
          logInfo "Add($REMOTE_USER): $(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos" >> $rosterLogFile
          #if [[ "$type" == "r" ]] ; then
          #  welcomeRegular $(trim $CGI_newemail)
          #else
          #  welcomeSpare $(trim $CGI_newemail)
          #fi
          sleep 1
          sendRegistrationEmail $(trim $CGI_newemail)
        else
          logWarning "Failed Add: Duplicate player: $(trim $CGI_newemail)" >> $rosterLogFile
        fi
      else
        logWarning "Failed Add: Unsafe player info: $(trim $CGI_newemail)~$CGI_fname~$CGI_lname~$type~$pos" >> $rosterLogFile
      fi
      ;;
  esac
cat << EOF
Status: 302 redirect
Location: roster.cgi

EOF
exit
fi
  
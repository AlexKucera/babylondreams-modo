#!/usr/bin/env bash
# Requires http://caspian.dotconf.net/menu/Software/SendEmail/

source /Volumes/ProjectsRaid/x_Pipeline/Scripting/tinkertoys/bash/mail_send.conf
SUBJECT="modo render completed"
MACHINE=$(hostname -s)


START=$(date +%s)
STARTDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")

@require(modo_cl, render_range, commands)
FRAMES=$((@render_range['first']!s-@render_range['last']!s+1))

@for command in commands:
"@modo_cl" < "@command"
@end



END=$(date +%s)
ENDDATE=$(date -j -f "%s" "`date +%s`" "+%A, %d.%m.%Y %T")
secs=$((END-START))
perframe=$(($secs/$FRAMES))
DURATION=$(printf '%dh:%02dm:%02ds' $(($secs/3600)) $(($secs%3600/60)) $(($secs%60)))
DURATIONPERFRAME=$(printf '%dh:%02dm:%02ds' $(($perframe/3600)) $(($perframe%3600/60)) $(($perframe%60)))

BODY="${MACHINE} just finished rendering sperrholz_09_v03.
It started at ${STARTDATE} and ended at ${ENDDATE} taking ${DURATION} overall for ${FRAMES} frames.
That's ${DURATIONPERFRAME} per frame on average."

sendemail -f ${FROM_ADDRESS} -t ${TO_ADDRESS} -m ${BODY} -u ${SUBJECT} -s ${SERVER} -xu ${USER} -xp ${PASS}
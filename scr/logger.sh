#!/usr/bin/env bash

COUNT=0
LOGFILE=/scr/logger.$(date +%Y-%m-%d).log

function main() {

	local REPOSITORY=$1
	local URL=$2
	local MEDIATYPE=$3
	local TAG=$4
	local DIGEST=$5
	local TIMESTAMP=$6
	local ACTOR=$7
	local ACTION=$8

	echo "----- Request Start ----->" >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " repository: " $REPOSITORY >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " url: " $URL >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " mediaType: " $MEDIATYPE >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " tag: " $TAG >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " digest: " $DIGEST >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " timestamp: " $TIMESTAMP >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " actor: " $ACTOR >> $LOGFILE
	echo $(date +%Y-%m-%d.%H-%M-%S.%N) " action: " $ACTION >> $LOGFILE
	echo "<----- Request End -----" >> $LOGFILE

	# .
	# . INSERT ADDITIONAL CODE HERE
	# .

    return $?

}

ARGS=( "$@" )

while [ "$1" != "" ]; do

	# echo "Received: ${1}"
	COUNT=$(($COUNT + 1))
	shift;

done

if [ $? -eq 0 ] && [ $COUNT == 8 ]; then main "${ARGS[@]}"; fi


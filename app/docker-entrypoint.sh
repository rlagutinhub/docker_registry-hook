#!/bin/bash

set -e
set -x

# VARIABLES

SCR=configure.py

APPDIR=/app
KEEPME=".keepme"

TOKEN=${TOKEN:-"empty"}
MAILSERVER=${MAILSERVER:-"empty"}
HOOKS=${HOOKS:-"empty"}
MAILPORT=${MAILPORT:-"empty"}
MAILFROM=${MAILFROM:-"empty"}
MAILTO=${MAILTO:-"empty"}

function CONFIGURE() {

    if [ "$TOKEN" == "empty" ] || [ "$MAILSERVER" == "empty" ] || [ "$HOOKS" == "empty" ] || [ "$MAILPORT" == "empty" ] || [ "$MAILFROM" == "empty" ] || [ "$MAILTO" == "empty" ]; then

        echo "Error: Stop deploy - Variables not defined."; exit 1

    else

        $(which python3) $SCR \
         -token $TOKEN \
         -mailserver $MAILSERVER \
         -hooks $HOOKS \
         -mailport $MAILPORT \
         -mailfrom $MAILFROM \
         -mailto $MAILTO

    fi

}

# $1 = $APPDIR
# $2 = $KEEPME
function FIRST_START_CONF() {

    CONFIGURE; touch $1/$2

}

# MAIN
# https://github.com/docker-library/official-images#consistency
# https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/#entrypoint
# https://github.com/CentOS/CentOS-Dockerfiles/tree/master/httpd/centos7

if [ "${1:0:1}" = '-' ]; then
    set -- python3 "$@"
fi

if [ "$1" = 'python3' ]; then

    if [ ! -f $APPDIR/$KEEPME ]; then
        FIRST_START_CONF $APPDIR $KEEPME
    fi

    shift
    set -- "$(which python3)" "$@"

fi

exec "$@"


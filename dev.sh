#!/bin/bash

RESTORE='\033[0m'
RED='\033[00;31m'
GREEN='\033[00;32m'
YELLOW='\e[0;33m'


# No one deserves to have to stay decorating command
# Instructions:
# 1) ". dev.sh 'nome do virtualenv'"
# 2) "devhelp"
# 3) Be happy

workon ${1}

export PROJ_BASE="$(dirname ${BASH_SOURCE[0]})"
CD=$(pwd)
cd $PROJ_BASE
export PROJ_BASE=$(pwd)
cd $CD

#. ci/funcs.sh

function devhelp {
    echo -e "${GREEN}devhelp${RESTORE}               Print this ${RED}help${RESTORE}"
    echo -e ""
    echo -e "${GREEN}run-unittests${RESTORE}         Run ${RED}unit tests${RESTORE}"
    echo -e ""
    echo -e "${GREEN}run-functionaltest${RESTORE}    Run ${RED}functional tests${RESTORE}"
    echo -e ""
    echo -e "${GREEN}run-djangoserver${RESTORE}      Run ${RED}backend${RESTORE} django server"
    echo -e ""
    echo -e "${GREEN}run-resetdatabase${RESTORE}     ${RED}Reset${RESTORE} the database"
    echo -e ""
}

function run-unittest {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "./manage.py test lists" "Unit Tests"
    exitcode=$?
    cd $CD
    return $exitcode
}

function run-functionaltest {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "./manage.py test functional_tests" "Functional Tests"
    exitcode=$?
    cd $CD
    return $exitcode
}

function run-djangoserver {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "./manage.py runserver" "Servidor django"
    exitcode=$?
    cd $CD
    return $exitcode
}

function run-resetdatabase {
    CD=$(pwd)
    cd $PROJ_BASE
    dorun "rm db.sqlite3" "Removing Database"
    dorun "./manage.py migrate --noinput" "Migrating Database"
    exitcode=$?
    cd $CD
    return $exitcode
}

function produce_alias {
    echo "----------------------------------------------------------------------"
    echo "The following command create an alias that you can use"
    echo "to goes on dev enviroment to this project from anywhere to to you bash."
    echo "Suggestion 1: add in your ~/.bashrc"
    echo "Suggestion 2: Change the alias name to anything more appropriate"
    echo "----------------------------------------------------------------------"
    echo_green "alias tddproject='cd $(readlink -e $PROJ_BASE) && . dev.sh tddpython'"
    echo "----------------------------------------------------------------------"
}

function echo_red {
    echo -e "${RED}$1${RESTORE}";
}

function echo_green {
    echo -e "${GREEN}$1${RESTORE}";
}

function echo_yellow {
    echo -e "${YELLOW}$1${RESTORE}";
}

function now_milis {
    date +%s%N | cut -b1-13
}

function dorun {
    cmd="$1"
    name="$2"
    echo ----------------------------------------------------------------------
    echo_green "STARTING $name ..."
    echo "$cmd"
    t1=$(now_milis)
    $cmd
    exitcode=$?
    t2=$(now_milis)
    delta_t=$(expr $t2 - $t1)
    if [ $exitcode == 0 ]
    then
        echo_green "FINISHED $name in $delta_t ms"
        echo ----------------------------------------------------------------------
    else
        echo_red "ERROR: $name (status: $exitcode, time: $delta_t ms)"
        echo ----------------------------------------------------------------------
        return $exitcode
    fi
}

echo_green "Welcome Jonatas Leon" # Change this for a friendliest welcome message
echo_green "Hint: autocomplete works with the following commands"
echo_red   "----------------------------------------------------------------------"
devhelp

#!/bin/bash
HOUNDSPLOIT_PATH="$HOME/.HoundSploit"
HOUNDSPLOIT_OLD_PATH="$HOME/HoundSploit"

if ! [ -f "$HOUNDSPLOIT_PATH/enable_root.cfg" ] && [ $(id -u) = 0 ] ; then
	echo "ERROR: This script must NOT be run as 'root'"
	exit 1
fi

if ! [ $(uname) == "Linux" ] ; then
    echo "ERROR: This installation script is only for systems running a Linux distribution"
    exit 1
fi

if ! [ -d "$HOUNDSPLOIT_PATH" ] ; then
    mkdir $HOUNDSPLOIT_PATH
fi

if ! [ -d "$HOUNDSPLOIT_PATH/exploitdb" ] ; then
    cd $HOUNDSPLOIT_PATH
    git clone https://github.com/offensive-security/exploitdb
else
    cd $HOUNDSPLOIT_PATH/exploitdb
    git_output=$(git pull)
	if [ "$git_output" == "Already up to date." ]  ; then
        echo "Database already up-to-date"
    else
        if [ -f "$HOUNDSPLOIT_PATH/hound_db.sqlite3" ] ; then
            rm $HOUNDSPLOIT_PATH/hound_db.sqlite3
        fi
        echo "Latest version of the database downloaded"
    fi
fi

if ! [ -d "$HOUNDSPLOIT_PATH/hsploit" ] ; then
    git clone https://github.com/nicolas-carolo/hsploit $HOUNDSPLOIT_PATH/hsploit
fi

cd $HOUNDSPLOIT_PATH/hsploit
git_output=$(git pull)
if [ "$git_output" == "Already up to date." ]  ; then
    echo "hsploit already up-to-date"
else
    echo "Latest version of hsploit downloaded"
    echo "Run the following commands (be sure to use the Python 3 interpreter)"
    echo -e "\t$ pip install -r $HOUNDSPLOIT_PATH/hsploit/requirements.txt"
    echo -e "\t$ cd $HOUNDSPLOIT_PATH/hsploit"
    echo -e "\t$ python setup.py install"
    echo -e "\t$ hsploit"
fi

if [ -d $HOUNDSPLOIT_OLD_PATH  ] ; then
    if [ -f "$HOUNDSPLOIT_OLD_PATH/custom_suggestions.csv" ] ; then
        cp $HOUNDSPLOIT_OLD_PATH/custom_suggestions.csv $HOUNDSPLOIT_PATH/custom_suggestions.csv
    fi
    if [ -d $HOUNDSPLOIT_OLD_PATH/hsploit  ] && ! [ -d $HOUNDSPLOIT_OLD_PATH/houndsploit  ] ; then
        rm -fr $HOUNDSPLOIT_OLD_PATH
        echo "Old HoundSploit's and hsploit's files have been removed"
    else
        rm -fr $HOUNDSPLOIT_OLD_PATH/hsploit
        echo "Old hsploit's files have been removed"
    fi
fi
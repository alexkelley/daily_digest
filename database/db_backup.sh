#!/bin/bash

#NOW=$(date +"%Y%m%dT%H%M%S")
NOW=$(date +%FT%T%Z )
BACKUPFILE="backup_$NOW.sql"

sqlite3 db.sqlite3 .dump > $BACKUPFILE

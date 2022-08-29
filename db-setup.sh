#!/bin/bash

psql -h db-postgres -U $PGUSER -d $PGDB -f /db-migrations/01.sql
psql -h db-postgres -U $PGUSER -d $PGDB -f /db-migrations/02.sql
psql -h db-postgres -U $PGUSER -d $PGDB -f /db-migrations/03_words.sql

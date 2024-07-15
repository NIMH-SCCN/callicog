#!/bin/bash

dotenv_path=".env"

if [ -f "$dotenv_path" ]; then

    # Export CalliCog environment variables for use in subsequent commands:

    # Enable automatic export of all variables
    set -a
    # Set (and export) CalliCog environment variables
    source .env
    # Disable automatic export of all variables
    set +a

    # Create user in Postgres:
    psql -h $CALLICOG_DB_HOST -p $CALLICOG_DB_PORT -U postgres -c "CREATE ROLE $CALLICOG_DB_USER WITH SUPERUSER LOGIN"

    # Create CalliCog database in Postgres
    createdb -h $CALLICOG_DB_HOST -p $CALLICOG_DB_PORT -U $CALLICOG_DB_USER $CALLICOG_DB_NAME

    # Subsitute database user in database schema file db.sql, then create schema in database:
    envsubst < $CALLICOG_DIR/src/db.sql | psql -h $CALLICOG_DB_HOST -U $CALLICOG_DB_USER -d $CALLICOG_DB_NAME
else
    echo "No .env in current directory. Change directory or create your .env."
fi

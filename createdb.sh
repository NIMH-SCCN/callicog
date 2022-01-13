#!/bin/bash

dropdb marmodb 2> /dev/null
createdb marmodb

psql -f db.sql -d marmodb
psql -f get_experiment_data.sql -d marmodb	

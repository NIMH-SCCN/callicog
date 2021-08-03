#!/bin/bash

dropdb marmodb 2> /dev/null
createdb marmodb
psql -f db.sql -d marmodb
	

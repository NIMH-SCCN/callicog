#!/bin/zsh

# Define environment variables for username, host, and database
PG_USER="sccn"
PG_HOST="localhost"
PG_DB="marmodb"

# Define the SQL command to select tables
SQL_COMMAND=$(cat <<-SQL
    SELECT table_name
    FROM information_schema.tables
    WHERE table_type = 'BASE TABLE'
    AND table_schema = 'public'
SQL
)

# Get the current date in YYYY_MM_DD format
CURRENT_DATE=$(date +"%Y_%m_%d")

# Define the output directory with the current date
OUTPUT_DIR="~/db_backup/marmodb/$CURRENT_DATE"

# Check if the output directory already exists
if [ -d "$OUTPUT_DIR" ]; then
    echo "Error: The output directory '$OUTPUT_DIR' already exists. Aborting."
    exit 1
fi

# Create the output directory
mkdir -p "$OUTPUT_DIR"

# Iterate through tables
for table in $(psql -U "$PG_USER" -h "$PG_HOST" -d "$PG_DB" -t -c "$SQL_COMMAND");
do
    # Dump the table to a SQL file in the specified output directory
    pg_dump -t "$table" -U "$PG_USER" -h "$PG_HOST" "$PG_DB" > "$OUTPUT_DIR/$table.sql"
done;

# Dump schema
pg_dump -U "$PG_USER" -h "$PG_HOST" "$PG_DB" --schema-only > "$OUTPUT_DIR/marmodb_schema.sql"

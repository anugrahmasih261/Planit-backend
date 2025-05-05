#!/bin/bash
echo "Initializing database..."
DB_PATH=${1:-"db.sqlite3"}  # Default to local db if no argument

mkdir -p $(dirname "$DB_PATH")
touch "$DB_PATH"
chmod 644 "$DB_PATH"
echo "Database initialized at $DB_PATH"
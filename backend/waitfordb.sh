#!/bin/sh

# The first time the database is created, it takes a little longer to set up.
# Even with the 'depends_on' directive in 'docker-compose.yaml', the Django
# container tries to connect to the database before it is initialized.
# With this script we make sure everything is up before we start Django.

function postgres_ready(){
python3 << END
import sys
import psycopg2
try:
    conn = psycopg2.connect(dbname="django", user="$DATABASE_USER", password="$DATABASE_PASS", host="db")
except psycopg2.OperationalError:
    sys.exit(1)
sys.exit(0)
END
}

until postgres_ready; do
    >&2 echo "Postgres is unavailable - sleeping"
    sleep 1
done

>&2 echo "Postgres is up - continuing..."

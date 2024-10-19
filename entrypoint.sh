#! /usr/bin/env bash
set -e
set -x

# Load environment variables if a .env file exists
if [ -f .env ]; then
    echo "Loading environment variables from .env file..."
    export $(grep -v '^#' .env | xargs)
fi

# Ensure mandatory environment variables are set
: "${OPENAI_API_KEY:?OPENAI_API_KEY not set}"
: "${DB_SERVER:?DB_SERVER not set}"
: "${DB_DATABASE:?DB_DATABASE not set}"
: "${DB_USER:?DB_USER not set}"
: "${DB_PASSWORD:?DB_PASSWORD not set}"

# Optional environment variables with default values
LOG_LEVEL=${LOG_LEVEL:-info}

# Start Gunicorn with the FastAPI app
echo "Starting Gunicorn with FastAPI..."
uvicorn app.main:app --reload --host=0.0.0.0 --port=8000

# gunicorn app.main:app

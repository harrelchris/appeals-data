#!/usr/bin/env bash

set -e

source .venv/bin/activate

echo "Updating sitemaps"
python -m app.sitemaps

#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r ./requirements/render.txt

# Convert static asset files
python manage.py collectstatic --no-input


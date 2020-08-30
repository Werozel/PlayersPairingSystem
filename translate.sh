venv/Scripts/activate
pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d translations -l ru
pybabel compile -f -d translations
pybabel update -i messages.pot -d translations
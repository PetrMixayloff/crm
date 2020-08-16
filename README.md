Python version for project 3.8

Install postgresql https://www.postgresql.org/download/

Create db and user:

`CREATE DATABASE baloon_crm;`

`CREATE USER baloon_crm_user WITH PASSWORD 'baloon_pass';`

`GRANT ALL PRIVILEGES ON DATABASE baloon_crm TO baloon_crm_user;`

Upgrade your pip version `python3 -m pip install --upgrade --user pip`

Install poetry `pip3 install poetry`

For creating virtual environment inside project `poetry config virtualenvs.in-project true`

For installation run `poetry install`

Activate virtual environment `source .venv/bin/activate`

Create .env file in root directory and fill values for db access (see .env_example).

Run server `python3 server.py`

To see docs open in browser http://127.0.0.1:8000/docs

Create migration `poetry run alembic revision --autogenerate -m 'description of migration'`

DB upgrade `poetry run alembic upgrade head`
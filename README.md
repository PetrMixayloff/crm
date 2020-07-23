Python version for project 3.8

We use poetry `pip3 install poetry`

For creating virtual environment inside project `poetry config virtualenvs.in-project true`

For installation run `poetry install`

Activate virtual environment `source .venv/bin/activate`

Create postgresql db.

Create .env file in root directory and fill values for db access (see .env_example).

Run server `uvicorn src.main.asgi:app --reload`

To see docs open in browser http://127.0.0.1:8000/docs
Python version for project 3.8

We use poetry `pip3 install poetry`

For creating virtual environment inside project `poetry config virtualenvs.in-project true`

For installation run `poetry install`

Activate virtual environment `source .venv/bin/activate`

Run server `uvicorn src.main.asgi:app --reload`
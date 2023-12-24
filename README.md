# postgres_async_template
Template Project for a fastapi app with asynchronous postgres db and alembic migrations

## Usage

The whole application can be started with `docker compose up -d --build`

### Start postgre database

Use the docker compose to initialize the database: `docker compose up -d --build db`  
When executing the backend locally, migrate to the latest version with `alembic upgrade head`

### Start the backend

- Use the docker composeto initialize the database: `docker compose up -d --build backend`
- Alternatively use the `backend\start_backend.py` to start the backend locally

### Create backend endpoints for frontend

Execute the script `frontend\create_backend_openapi_template.sh` to auto-generate a template of the backend app for a frontend service.

### Testing

In the `tests\backend_tests` execute `pytest` after starting a database and backend instance to run all unit tests.
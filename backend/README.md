# Alembic
The database is set up with the migration tool alembic.  
When starting the database for the first time or changing the database models please make sure to create a database revision and apply the revision.  
Alembic settings can be configured in `backend\alembic.ini`

## Usage
- Start postgres `docker compose up -d db`
- Create a database revision `alembic revision --autogenerate -m "testrevision"`
- Apply a database revision `alembic upgrade head`
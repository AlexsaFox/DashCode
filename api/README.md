# API part of DashCode

## Prepare environment
### Development
1. Prepare python virtual environment
```bash
python -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```
2. Start development containers (Redis and PostgreSQL)
```bash
docker-compose -f dev-compose.yaml up
```
3. Upgrade database using alembic revisions
```bash
alembic upgrade head
```
4. Run applications
```bash
python run.py
```

## Working with database
### Alembic 
* Create new revision (migration)
```bash
alembic revision --autogenerate -m "<your message here>"
```
* Upgrade database
```bash
alembic upgrade head            # Upgrade to latest version
alembic upgrade <revision>      # Specify revision
```

### Connect to PostgreSQL database inside docker container
```bash
docker-compose -f dev-compose.yaml exec -it postgres psql -h localhost -U <username> -d <database>
```
## Testing
### Run tests
* Run all tests; show detailed output
```bash
pytest -vvv
```
* Run one specific test
```bash
pytest -k "test_registration_duplicate_username"
```

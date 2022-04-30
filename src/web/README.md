# Web interface and API
## Setup
1. Make sure you're in the app root (the same directory with ```run.py``` file)
2. Create and activete virtual environemnt:
```bash
$ python3 -m venv .venv
$ source ./venv/bin/activate    # Linux
$ ./venv/Scripts/activate       # Windows
```
3. Install pip packages
```bash
$ pip install -r requirements.txt
```
4. Create .env file with environment variables (example could be found in .env.example)
5. Create the database:
```bash
$ flask db init
$ flask db migrate
$ flask db upgrade
```
6. Start application:
```bash
$ flask run
``` 
or 
```bash
$ python run.py
```

## API request structure
Most request are avaliable only with API authentication tokens. These tokens must be passed in "Authorization" header with "Bearer" type. Consider following CURL example:
```bash
curl -X POST -i -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJrZXkiOiJITnJpZFFDWFVFQm9pV3h3QXJNZVlVdHhOZHRZa1ZJbCIsImV4cCI6MTY0OTk1MTE0OH0.Y4wNi4TkcGzLY-q7pTg6Au_tXQMeOXoN0psshC8cFso" http://127.0.0.1:5000/api/whoami
```
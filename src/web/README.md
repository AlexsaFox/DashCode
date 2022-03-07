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
```
$ pip install -r requirements.txt
```
4. Create .env file with environment variables (example could be found in .env.example)
5. Create the database:
```
$ flask db init
$ flask db migrate
$ flask db upgrade
```
6. Start application:
```
$ flask run
``` 
or 
```
$ python run.py
```

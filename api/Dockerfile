FROM python:3.10-slim-bullseye

WORKDIR /app
COPY . .
RUN pip install -qr requirements.txt
RUN alembic upgrade head

CMD [ "gunicorn", "run:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker" ]

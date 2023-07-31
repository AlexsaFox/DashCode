FROM python:3.10-slim-bullseye

RUN apt update
RUN apt install gcc -y

WORKDIR /app
COPY . .
RUN pip install -qr requirements.txt --use-feature=no-binary-enable-wheel-cache asyncpg

CMD [ "sh", "-c", "alembic upgrade head; gunicorn -b $API_server__host:$API_server__port run:app -w 4 -k uvicorn.workers.UvicornWorker" ]

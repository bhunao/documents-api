FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

COPY ./requirements.txt /app/requirements.txt
COPY ./prestart.sh /app/prestart.sh

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app /app

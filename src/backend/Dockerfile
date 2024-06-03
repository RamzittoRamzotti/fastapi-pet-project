FROM python:3.12

WORKDIR /app

COPY . /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

ENTRYPOINT ["uvicorn", "app.main:app",  "--host", "0.0.0.0", "--port", "8000"]

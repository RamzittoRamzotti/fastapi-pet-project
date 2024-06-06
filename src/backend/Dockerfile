FROM python:3.12

WORKDIR /app

COPY . .

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "5000"]

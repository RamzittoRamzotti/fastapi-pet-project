FROM python:3.12

WORKDIR /app

EXPOSE 5000

COPY . .

COPY ./requirements.txt /app/requirements.txt

RUN pip install --upgrade pip && pip install -r requirements.txt

ENTRYPOINT ["fastapi","dev", "main.py"]

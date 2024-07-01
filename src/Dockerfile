FROM python:3.12

WORKDIR /app/src/

COPY backend ./backend
COPY frontend/public/images ./frontend/public/images

WORKDIR /app/src/backend

RUN pip install --upgrade pip && pip install -r requirements.txt


COPY backend/scr.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]
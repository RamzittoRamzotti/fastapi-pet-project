FROM node:lts-alpine as build

WORKDIR /app

COPY frontend/package*.json ./

RUN npm install

COPY . .

RUN npm run build

FROM nginx:alpine


COPY ./frontend/.nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html


ENTRYPOINT ["nginx", "-g", "daemon off;"]
FROM node:lts-alpine as build

WORKDIR /app

COPY . .

RUN npm install && npm run build

FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html
COPY --from=build /app/.nginx/nginx.conf /etc/nginx/sites-enabled/default

WORKDIR /usr/share/nginx/html


ENTRYPOINT ["nginx", "-g", "daemon off;"]
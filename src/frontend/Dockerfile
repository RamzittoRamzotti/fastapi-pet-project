FROM node:lts-alpine as build

WORKDIR /app

COPY . .

RUN npm install && npm run build

FROM nginx:stable-alpine
COPY --from=build /app/build /var/www/build
COPY --from=build /app/.nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html


ENTRYPOINT ["nginx", "-g", "daemon off;"]
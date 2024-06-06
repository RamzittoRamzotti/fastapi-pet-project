FROM nginx:latest

COPY ./nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html

RUN rm -rf ./*


EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]
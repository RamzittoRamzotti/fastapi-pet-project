# 2. For Nginx setup
FROM nginx:alpine

# Copy config nginx
COPY ./frontend/.nginx/nginx.conf /etc/nginx/conf.d/default.conf

WORKDIR /usr/share/nginx/html


# Containers run nginx with global directives and daemon off
ENTRYPOINT ["nginx", "-g", "daemon off;"]
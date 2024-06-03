FROM node:14

WORKDIR /app

COPY ./package.json /app/package.json

COPY ./package-lock.json /app/package-lock.json

RUN npm install

COPY . /app

RUN npm run build

CMD ["npx", "serve", "-s", "build"]
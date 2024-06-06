FROM node:14 as build

WORKDIR /app

COPY package.json package-lock.json ./

RUN npm install

COPY . .

RUN npm run build

VOLUME ./build ./build

CMD ["npx", "serve", "-s", "build"]




FROM node:18

WORKDIR /api

ENV EXPRESS_PORT=80

EXPOSE 80

COPY ./package.json ./package-lock.json ./

RUN npm install

COPY ./app.mjs .

CMD ["node", "app.mjs"]

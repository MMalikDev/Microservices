ARG VERSION=20-bookworm-slim
FROM node:$VERSION as builder

WORKDIR /server
COPY package*.json ./

RUN npm install

# ------------------------------ #

FROM builder AS production

ENV NODE_ENV production

COPY . .

CMD [ "npm", "start" ]

FROM node:18-alpine AS build
WORKDIR /app
COPY package* .
RUN npm install
COPY postcss.config.js .
COPY tailwind.config.js .
COPY public ./public
COPY src ./src
RUN npm run build

FROM caddy:alpine
COPY --from=build /app/build /usr/share/caddy
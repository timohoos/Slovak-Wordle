FROM node:18-alpine AS build
WORKDIR /app
COPY package* ./
RUN npm install
COPY postcss.config.js ./
COPY tailwind.config.js ./
COPY public ./public
COPY src ./src
ARG BACKEND_URL
ENV REACT_APP_BACKEND_URL=$BACKEND_URL
RUN npm run build

FROM caddy:alpine
COPY --from=build /app/build /app
COPY Caddyfile /etc/caddy/
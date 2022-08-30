#!/bin/bash

rsync -av --exclude='frontend/node_modules' --exclude='frontend/build' \
      backend frontend utils db-migrations docker-compose.production.yaml db-setup.sh \
      root@slovodna.sk:Slovak-Wordle
ssh root@slovodna.sk 'mv Slovak-Wordle/docker-compose.production.yaml Slovak-Wordle/docker-compose.yaml'
ssh root@slovodna.sk 'mv Slovak-Wordle/frontend/Caddyfile.production Slovak-Wordle/frontend/Caddyfile'
ssh root@slovodna.sk 'cd Slovak-Wordle && docker-compose build'
ssh root@slovodna.sk 'cd Slovak-Wordle && docker-compose up -d'

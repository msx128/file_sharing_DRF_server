#!/usr/bin/env fish
source ./.venv/bin/activate.fish
docker compose up -d
docker compose ps

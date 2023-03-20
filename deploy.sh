#!/bin/sh
git pull
sudo docker-compose -f ./docker-compose.prod.yml up --build -d

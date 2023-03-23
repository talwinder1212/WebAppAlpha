#!/bin/bash

cd /var/www/html
docker-compose down
docker-compose up -d

#!/bin/bash

pip3 freeze > ./requirements.txt
cd Password-Manager
docker-compose up -d
cd ..

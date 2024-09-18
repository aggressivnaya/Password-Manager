#!/bin/bash

pip3 freeze > requirements.txt
docker-compose up -d

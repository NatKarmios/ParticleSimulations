#!/usr/bin/env bash

# Open port 5000 on localhost
docker run --restart=always -d -v $PWD/cfg:/root/cfg -p 127.0.0.1:5000:5000 --name particles natk/particles

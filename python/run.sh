#!/usr/bin/env bash

# Open port 5000 on localhost
docker run -v ./cfg -p 127.0.0.1:5000:5000 natk/particles

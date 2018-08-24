#!/bin/bash

echo "Docker login can fail"
docker login
docker build -t kylews/huskyblog .
docker push kylews/huskyblog

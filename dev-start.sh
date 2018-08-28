#!/bin/bash
./build.sh
#openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 -subj "/CN=localhost" -keyout TLS/privkey.pem -out TLS/fullchain.pem
# Remove old stuff
docker rm -f dock_huskyblog
docker rm -f mongo-server
docker network rm husky_network
# netowrk create
docker network create husky_network
# Mongodb
docker run -d --name mongo-server -p 27017:27017 --network husky_network mongo
docker run --name dock_huskyblog \
-p 6543:6543 \
-v /Users/kylews/go/src/github.com/KyleWS/huskyblog/huskyblog/app \
--network husky_network \
-d kylews/huskyblog


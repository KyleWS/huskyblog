#!/bin/bash

./build.sh

ssh root@142.93.21.143 '
docker rm -f dock_huskyblog
docker rm -f mongo-server
docker network rm husky_network
docker network create husky_network
docker run -d --name mongo-server -p 27017:27017 --network husky_network mongo
docker pull kylews/huskyblog
docker run --name dock_huskyblog \
-p 443:443 \
-p 6543:6543 \
-v /etc/letsencrypt/live/huskyexperience.net/fullchain.pem:/TLS/fullchain.pem \
-v /etc/letsencrypt/live/huskyexperience.net/privkey.pem:/TLS/privkey.pem \
--network husky_network \
-d kylews/huskyblog'

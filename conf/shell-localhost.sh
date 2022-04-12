#!/bin/bash
dockerid=`docker ps | grep w2p-docker | cut -f1 -d' '`
echo id docker $dockerid
docker exec -t -i $dockerid bash
exit 0
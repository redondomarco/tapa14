#!/bin/bash
dockerid=`docker ps | grep w2p-docker | cut -f1 -d' '`
echo id docker $dockerid
docker exec -t -i $dockerid python3 web2py.py -M -S tapa14
exit 0

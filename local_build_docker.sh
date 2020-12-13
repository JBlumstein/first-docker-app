#!/bin/bash
cd container
docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t jonahblumstein/$1 .
docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m --name $1 jonahblumstein/$1
#!/bin/bash
cd container
docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t jonahblumstein/$repo_name .
docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m --name $repo_name jonahblumstein/$repo_name
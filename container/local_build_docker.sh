#!/bin/bash
docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t jonahblumstein/bookrecoapp .
docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m --name bookrecoapp jonahblumstein/bookrecoapp
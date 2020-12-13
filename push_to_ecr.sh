#!/bin/bash

# switch to container folder
cd container

# log in
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin $repo_image

# build the image
docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t $1:$repo_tag .
docker tag $1:$repo_tag $repo_image/$1:$repo_tag
docker push $repo_image/$1:$repo_tag
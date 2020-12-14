#!/bin/bash

# switch to container folder
cd container

# log in
aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $repo_image

# create repository in ecr
aws ecr create-repository --repository-name $repo_name

# build the image
docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t $repo_name:$repo_tag .
docker tag $repo_name:$repo_tag $repo_image/$repo_name:$repo_tag
docker push $repo_image/$repo_name:$repo_tag
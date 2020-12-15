# Book recommender on ECS

## Project Context

For the last year, I've been a contractor for Equinox, a chain of fitness clubs based in NY and with locations around the world. One major ongoing initiative there is to build two apps: an iOS and Android-based general fitness application called Variis, and a SoulCycle (an Equinox brand) at-home stationary bike. 

As a data scientist and engineer, one of my responsibilities has been to create batched content recommendations for users, matching each user with exercise classes they might like. Most of these recommendations have been made on relatively simple criteria, such as most popular classes in your favorite exercise category (running, strength, cycling, yoga, etc.). These recommendations are usually created with an Athena query kicked off by an AWS lambda.

At various points in the last year, we've looked to create more sophisticated recommendations, based on recommender system techniques such as collaborative filtering. On a very applied level, in a content recommendation context, collaborative filtering entails finding similarities between users, and then recommending pieces of content to each user based on what similar users liked or did.

However, because collaborative filtering is an intensive process and on our dataset could eventually require a greater run-time than the 15 minute limit for a lambda, we've considered using ECS to deploy a collaborative filtering-based recommendation engine. However, due to my inexperience with Docker and ECS, this has always been a task too time consuming to be worth taking time away from other tasks for what could be only a marginal lift in user experience.

With the opportunity to build something from scratch in Harvard Extension School's CSCI-E90 (Cloud Services and Infrastructure) final project, I no longer had this excuse, since I would be building a recommender system on my own time. For the project, I decided to build something similar to what we would want at work, using a different dataset: a compendium of 25M book reviews on GoodReads.

In order to keep things simple, I chose *implicit* collaborative filtering, making recommendations for what users might want to read based on what similar users read in the past.

## Building locally

This project consisted of two main challenges: building the docker container, and posting it to ECR and running it on ECS. 

The former proved much easier than the latter. To build the container that creates a model and saves it to a pickle file and then runs it in a docker container, all I needed to do was create a python file that did the work (app/container/app.py), a requirements file for the package imports I used (app/requirements.txt),a Dockerfile defining how to build the image (app/Dockerfile), a shell script to build the image locally and create a container to run the image in (local_build_docker.sh). I also created a config file to hold my environment variables (not submitted as it contains my AWS secrets) to hold environment variables used throughout the repo.

I'm going to hold off on going through my scripts for this part, as they are entirely non-cloud related.

## Moving to the cloud

Working with docker on AWS was tougher, but I ultimately succeeded to posting my docker image to ECR and then running it in ECS using only CLI commands.

### Posting to ECR

To post my docker image to ECR, I built a short shell script, with the following steps:

Set up, by reading in my environment variables and switching into my container folder (which contains the contents of my docker image):

    #!/bin/bash
    source config
    cd container

Next I logged in to AWS:

    aws ecr get-login-password --region $aws_region | docker login --username AWS --password-stdin $repo_image

I then built my repo in ECR:
    
    aws ecr create-repository --repository-name $repo_name

I next built my image with my argument values (ARGs in my Dockerfile) and tagged it:

    docker build --build-arg aws_key=$AWSAccessKeyId --build-arg aws_secret=$AWSSecretKey -t $repo_name:$repo_tag .
    docker tag $repo_name:$repo_tag $repo_image/$repo_name:$repo_tag

Finally, I pushed my image to ECR:
    
    docker push $repo_image/$repo_name:$repo_tag

### Running on ECS

The toughest part, by a good margin, was figuring out how to run my image, now in ECR, on ECS. In order to simplify things, I used Fargate, but I still needed a fairly lengthy shell script, a json file, and a Python script to build a task definition, to get it done from the CLI.

Let's dig
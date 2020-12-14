#!/bin/bash
source config

# get datetime
dtnow="`date +%Y%m%d%H%M%S`"

# create policy if none exists
aws iam --region $aws_region create-role --role-name $role_name --assume-role-policy-document file://task-execution-assume-role.json
aws iam --region $aws_region attach-role-policy --role-name $role_name --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# create a cluster
aws ecs create-cluster --cluster-name $cluster_name --capacity-providers FARGATE

# fill out task definition template
python3 update_task_definition.py $dtnow

# register a task definition
aws ecs register-task-definition --cli-input-json file://updated-task-definition.json

# start task in cluster
aws ecs start-task 
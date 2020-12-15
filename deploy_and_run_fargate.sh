#!/bin/bash
source config

# get datetime
dtnow="`date +%Y%m%d%H%M%S`"
container_name_dt=$container_name-$dtnow

# create policy if none exists
aws iam --region $aws_region create-role --role-name $role_name --assume-role-policy-document file://task-execution-assume-role.json
aws iam --region $aws_region attach-role-policy --role-name $role_name --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# fill out task definition template
python3 update_task_definition.py $container_name_dt

# create a cluster
aws ecs create-cluster --cluster-name $cluster_name --capacity-providers FARGATE 

# create a log group
aws logs create-log-group --log-group-name $log_group_name

# register a task definition
aws ecs register-task-definition --cli-input-json file://updated_task_definition.json

# run task in cluster
aws ecs run-task --launch-type FARGATE --task-definition $task_definition_name --cluster arn:aws:ecs:$aws_region:$aws_account_id:cluster/$cluster_name --network-configuration "awsvpcConfiguration={subnets=[$subnet1,$subnet2],securityGroups=[$security_group],assignPublicIp=ENABLED}"
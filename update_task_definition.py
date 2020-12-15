import json
import os
import sys
from datetime import datetime

def parse_config(file_name='config'):
    conf = {}
    with open(file_name) as fp:
        for line in fp:
            key, val = line.strip().split('=', 1)
            conf[key] = val
    return conf

# read in container name with dt
container_name = str(sys.argv[1])

# parse config
env_vars = parse_config()

# fill in environment variables
role_name = env_vars['role_name']
aws_account_id = env_vars['aws_account_id']
aws_region = env_vars['aws_region']
repo_image = env_vars['repo_image']
repo_name = env_vars['repo_name']
repo_tag = env_vars['repo_tag']
task_definition_name = env_vars['task_definition_name']
log_group_name = env_vars['log_group_name']
role_name = env_vars['role_name']

template = {
	"executionRoleArn": f"arn:aws:iam::{aws_account_id}:role/{role_name}",
	"containerDefinitions": [{
		"logConfiguration": {
			"logDriver": "awslogs",
			"options": {
				"awslogs-group": log_group_name,
				"awslogs-region": aws_region,
				"awslogs-stream-prefix": "ecs"
			}
		},
		"image": f"{repo_image}/{repo_name}:{repo_tag}",
		"name": container_name
	}],
	"memory": "8192",
	"taskRoleArn": f"arn:aws:iam::{aws_account_id}:role/{role_name}",
	"family": task_definition_name,
	"requiresCompatibilities": ["FARGATE"],
	"networkMode": "awsvpc",
	"cpu": "2048"
}

# write out update task definition
with open('updated_task_definition.json', 'w') as outfile:
    json.dump(template, outfile)
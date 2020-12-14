import json
import os
import sys
from datetime import datetime

# fill in environment variables
role_name = os.environ['role_name']
aws_account_id = os.environ['aws_account_id']
aws_region = os.environ['aws_region']
repo_image = os.environ['repo_image']
repo_name = os.environ['repo_name']
repo_tag = os.environ['repo_tag']
task_definition_name = os.environ['task_definition_name']

# use current datetime in naming
dt_now = str(sys.argv[1])

# read in task definition template
with open('task_definition_template.json') as template_file: 
    template = json.load(template_file)

# fill in template
template['executionRoleArn'] = template['executionRoleArn'].replace('account_id', aws_account_id).replace('role_name', role_name)
template['containerDefinitions'][0]['image'] = template['containerDefinitions'][0]['image'].replace('account_id', aws_account_id).replace('repo_image', repo_image).replace('repo_name', repo_name).replace('repo_tag', repo_tag)
template['containerDefinitions'][0]['name'] = template['containerDefinitions'][0]['name'] + '-' + dt_now
template['taskRoleArn'] = template['taskRoleArn'].replace('account_id', aws_account_id).replace('role_name', role_name)
template['taskDefinitionArn'] = template['taskDefinitionArn'].replace('aws_region', aws_region).replace('account_id', aws_account_id).replace('task_definition_name', task_definition_name)
template['family'] = task_definition_name
template['containerDefinitions'][0]['logConfiguration']['options']['awslogs-group'] = template['containerDefinitions'][0]['logConfiguration']['options']['awslogs-group'].replace('task_definition_name', task_definition_name)
template['containerDefinitions'][0]['logConfiguration']['options']['awslogs-region'] = aws_region

# write out update task definition
with open('updated_task_definition.json', 'w') as outfile:
    json.dump(template, outfile)
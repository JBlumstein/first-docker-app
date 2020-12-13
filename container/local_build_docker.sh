#!/bin/bash
docker build -t jonahblumstein/myfirstapp .
docker run -it --log-opt mode=non-blocking --log-opt max-buffer-size=4m -e AWS_KEY=$AWSAccessKeyId -e AWS_SECRET=$AWSSecretKey --name myfirstapp jonahblumstein/myfirstapp
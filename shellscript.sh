#!/bin/bash
cd home/ec2-user
sudo yum install -y python3
python3 -m pip install boto3 --user
aws s3 cp s3://mys3cloudbucket/CND.py CND.py
python3 CND.py
# aws s3 cp output.txt s3://mys3cloudbucket/output.txt
# python3 terminate.py

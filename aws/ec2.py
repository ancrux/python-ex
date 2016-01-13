# -*- coding: utf-8 -*-
"""
Documentation:
https://boto3.readthedocs.org/en/latest/index.html

- create user/access_key/access_secret create via console => IAM
- default config: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
- disable it when not used (e.g after deployment) for maximum security  
"""
import boto3

ec2 = boto3.resource('ec2')

# show all EC2 instances
instances = ec2.instances.all()
for instance in instances:
    print(instance.id, instance.instance_type)
    




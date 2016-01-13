# -*- coding: utf-8 -*-
"""
Documentation:
https://boto3.readthedocs.org/en/latest/index.html

- create user/access_key/access_secret create via console => IAM
- default config: https://boto3.readthedocs.org/en/latest/guide/quickstart.html#configuration
- disable it when not used (e.g after deployment) for maximum security  
"""
import boto3
from pprint import pprint


ec2 = boto3.resource('ec2')

# show all EC2 instances
instances = ec2.instances.all()
for instance in instances:
    # Ref: https://boto3.readthedocs.org/en/latest/reference/services/ec2.html#instance
    # Note: instance name is stored in tags(list) with key: 'Name'
    """
    # list all instance attributes
    print "=========="
    for attr in (attr for attr in dir(instance) if not attr.startswith('__')):
        print "%s = %s" % (attr, getattr(instance, attr))
    """
    print(instance.id, instance.instance_type, instance.tags)
    




#!/usr/bin/python
__author__ = 'monk-ee'

import yaml
import cherrypy
import boto.ec2
from boto.vpc import VPCConnection



#load configuration
configStream = open('config/config.yml', 'r')
configObj = yaml.load(configStream)

#print configObj['regions'][0]['name']

#conn = boto.ec2.connect_to_region(aws_access_key_id=configObj['keys'][0]['aws_access_key'],
#                                  aws_secret_access_key=configObj['keys'][0]['aws_secret_key'])

#print conn

regions = boto.ec2.regions(aws_access_key_id=configObj['keys'][0]['aws_access_key'],
                       aws_secret_access_key=configObj['keys'][0]['aws_secret_key'])

print regions

conn = VPCConnection(aws_access_key_id=configObj['keys'][0]['aws_access_key'],
                    aws_secret_access_key=configObj['keys'][0]['aws_secret_key'],
                    region=regions[1],
                    proxy='bne-app-proxy.au.fcl.internal',
                    proxy_port=3128
                    )
filter = [('state','available')]

vpc_status_list = conn.get_all_vpcs(None, filter)

#print type(vpc_status_list)

for vpc in vpc_status_list:
    for tag,value in vpc.tags.items():
        print tag+ " value: "+value
    subnet_filter =  [('vpcId',vpc.id)]
    vpc_subnets_list = conn.get_all_subnets(None, subnet_filter)
    print vpc_subnets_list


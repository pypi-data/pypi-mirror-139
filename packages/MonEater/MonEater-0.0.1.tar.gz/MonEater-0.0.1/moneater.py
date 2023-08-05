#!/usr/bin/env python

from influxdb import InfluxDBClient

import importlib
import datetime
import argparse
import sys

parser = argparse.ArgumentParser(description='Send cin to InfluxDB')
parser.add_argument('eater', help='Class responsible for eating data.')
parser.add_argument('--host',default='localhost', help='Host with InfluxDB')
parser.add_argument('--port','-p',default=8086,type=int, help='Port with InfluxDB')
parser.add_argument('--user','-u',default='root', help='InfluxDB user')
parser.add_argument('--password' ,default='root', help='InfluxDB password')
parser.add_argument('--database','-d',default='example', help='Target database')
parser.add_argument('--table','-t',default='measurement', help='Measurement name')
parser.add_argument('--tag',action='append', help='Tag for every measurement in format TAG=VALUE')

args = parser.parse_args()

#
# Tags
if args.tag:
    tags = {opt.split('=')[0]:opt.split('=')[1] for opt in args.tag}
else:
    tags = {}

#
# Eater
eater_parts =args.eater.split('.')
eater_module='.'.join(eater_parts[:-1])
eater_class =eater_parts[-1]
eater_module=importlib.import_module(eater_module)

eater=getattr(eater_module, eater_class)()

#
# Client
client = InfluxDBClient(args.host, args.port, args.user, args.password, args.database)

#
# The big loop
for line in sys.stdin:
    line=line.strip()
    print(line)
    if line=='': continue

    # parse
    points=eater.parse_line(line)
    if points==None: continue # No new data

    # Turn into a list
    if type(points)!=list:
        points=[points]

    # Check if they are only points or the full format
    now=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    points=[{'time':now, 'fields': point } if 'fields' not in point else point for point in points]

    # Add tags and table
    for point in points:
        mytags=tags.copy()
        if 'tags' in point:
            mytags.update(point['tags'])
        point.update({
            'measurement':args.table,
            'tags'       :mytags
        })

    # Upload
    print(points)
    client.write_points(points)

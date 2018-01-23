
from kafka import KafkaConsumer
import json
import requests
import time
import datetime
import argparse
from datadog import statsd
import boto3
import time

parser = argparse.ArgumentParser(description='Take variables for writing to s3.')
parser.add_argument('-add','--ip_address', help='IP address for kafka broker', required=True, type=str)
parser.add_argument('-mins','--minutes_to_collect', help='number of minutes back to collect', required=True, type=str)
parser.add_argument('-top','--topic', help='topic to consume', required=True, type=str)
parser.add_argument('-bucket','--s3_bucket', help='s3 bucket to write to', required=True, type=str)
args = parser.parse_args()

s3 = boto3.resource('s3')

def increment():
	statsd.increment('weather_sender.s3_write_success')

time_start = datetime.datetime.utcnow()
time_x_minutes = time_start + datetime.timedelta(minutes = args.mins)

consumer = KafkaConsumer(args.top, auto_offset_reset='earliest', group_id="weather-getter", bootstrap_servers=args.add)
with open('writing_file.json', 'w') as file:
	for msg in consumer:
		file.write(msg.value.decode('UTF-8'))
		file.write('\n')
		time_val = datetime.datetime.utcnow() < time_x_minutes
		if not time_val:
			break

bucket = s3.Bucket('weather-data-lindy')
bucket.put_object(Key="weather-data/{}.json".format(int(time.time())), Body=open("writing_file.json", 'rb'))
increment()

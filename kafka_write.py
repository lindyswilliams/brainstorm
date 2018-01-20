from kafka import KafkaProducer
import json
import requests
import time
import datetime
import argparse

parser = argparse.ArgumentParser(description='Take in api key and ip address.')
parser.add_argument('-key','--api_key', help='API key for openweathermap', required=True, type=str)
parser.add_argument('-add','--ip_address', help='IP address for kafka broker', required=True, type=str)
args = parser.parse_args()

try:
	while True:
		api_key = args.key
		response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=Denver&appid={}'.format(api_key))
		json_data = json.loads(response.text)
		producer = KafkaProducer(bootstrap_servers=args.add, value_serializer=lambda v: json.dumps(v).encode('utf-8'))
		producer.send('weather_data', json_data)
		time.sleep(60)
except:
	print("Exception")
	print(datetime.datetime.utcnow())
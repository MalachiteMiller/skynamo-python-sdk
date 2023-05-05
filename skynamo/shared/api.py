import os
import sys
from typing import Literal, Any, Union, Dict

import requests

from .helpers import updateEnvironmentVariablesFromJsonConfig


class SkynamoApiException(Exception):
	pass


def get_api_base():
	region = os.environ.get('SKYNAMO_REGION')
	if region is None:
		updateEnvironmentVariablesFromJsonConfig()
		region = os.environ.get('SKYNAMO_REGION')
	return f'https://api.{region}.skynamo.me/v1/'


def get_headers():
	instance_name = os.environ.get('SKYNAMO_INSTANCE_NAME')
	api_key = os.environ.get('SKYNAMO_API_KEY')
	if instance_name is None or api_key is None:
		updateEnvironmentVariablesFromJsonConfig()
		instance_name = os.environ.get('SKYNAMO_INSTANCE_NAME')
		api_key = os.environ.get('SKYNAMO_API_KEY')
	return {'x-api-client': instance_name, 'x-api-key': api_key, 'accept': 'application/json'}


def makeRequest(method: Literal['get', 'post', 'patch', 'put'], data_type: str, data: str = "", params: Dict = {}):
	print(' '.join([method, data_type, data, str(params)]))
	updateEnvironmentVariablesFromJsonConfig()
	timeout = int(os.environ.get('REQUESTS_TIMEOUT'))
	response = requests.request(method, get_api_base() + data_type, headers=get_headers(), data=data, params=params,
								timeout=timeout)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError as err:
		sys.tracebacklimit = 0
		raise SkynamoApiException('makeRequest ' + str(err.response.status_code) + ': ' + err.response.text + '; '
								  + err.response.url) from None
	return response.json()

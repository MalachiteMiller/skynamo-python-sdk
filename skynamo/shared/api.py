import os
import sys
from typing import Literal, Any, Union, Dict

import requests

from .helpers import updateEnvironmentVariablesFromJsonConfig


class SkynamoApiException(Exception):
	def __init__(self, message: str, status_code: int):
		super().__init__(message)
		self.status_code = status_code
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


def makeRequest(method: Literal['get', 'post', 'patch', 'put'], data_type: str, data: str = "", params: Dict = None,
				key: str = None):
	print(' '.join([method, data_type, data, str(params)]))
	updateEnvironmentVariablesFromJsonConfig(key)
	timeout = int(os.environ.get('REQUESTS_TIMEOUT'))
	response = requests.request(method, get_api_base() + data_type, headers=get_headers(), data=data, params=params,
								timeout=timeout)
	try:
		response.raise_for_status()
	except requests.exceptions.HTTPError as err:
		sys.tracebacklimit = 0
		raise SkynamoApiException('makeRequest ' + str(err.response.status_code) + ': ' + err.response.text + '; '
								  + err.response.url, err.response.status_code) from None
	return response.json()

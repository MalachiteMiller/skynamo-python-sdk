import os
from typing import Literal, Any, Union, Dict

import requests

from .helpers import updateEnvironmentVariablesFromJsonConfig


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


def makeRequest(method: Literal['get', 'post', 'patch', 'put'], data_type: str,
				data_or_params: Union[list, Dict[str, Any]] = ''):
	print(' '.join(filter(None, [method, data_type, str(data_or_params)])))
	response = requests.request(method, get_api_base() + data_type, headers=get_headers(), params=data_or_params,
								timeout=300)
	response.raise_for_status()
	return response.json()
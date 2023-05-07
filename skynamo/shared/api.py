import os
import sys
from typing import Literal, Any, Union, Dict

import requests

from .helpers import updateEnvironmentVariablesFromJsonConfig


class SkynamoApiException(Exception):
	"""Exception raised when the api returns an error

	Args:
		message: the error message
		status_code: the http status code of the error

	Attributes:
		status_code: the http status code of the error
	"""
	def __init__(self, message: str, status_code: int = 0):
		super().__init__(message)
		self.status_code = status_code


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
				verbose: Literal['t', 'l', 'f'] = 't', key: str = None) -> Dict:
	"""Makes a request to the Skynamo api.

	Args:
		method: get, post, patch, put.
		data_type: the api endpoint to call.
		data: a json string to pass to the api.
		params: a dict of parameters to pass to the api.
		verbose: Only used for writes. t=true, l=limited, f=false. Default is true.
		key: the api key to use, specified by its key in the json config file.

	Returns:
		The json response from the api.

	Raises:
		SkynamoApiException: Raised when the api returns an error.
	"""
	if verbose == 't':
		print(' '.join([method, data_type, data, str(params)]))
	elif verbose == 'l':
		print(' '.join([method, data_type]))
	else:
		pass
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

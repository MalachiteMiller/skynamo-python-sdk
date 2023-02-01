import requests
import json,math
import threading
import os
from typing import Literal,Union
from .helpers import updateEnvironmentVariablesFromJsonConfig

def getApiBase():
	region=os.environ.get('SKYNAMO_REGION')
	if region==None:
		updateEnvironmentVariablesFromJsonConfig()
		region=os.environ.get('SKYNAMO_REGION')
	return f'https://api.{region}.skynamo.me/v1/'

def getHeaders():
	instanceName=os.environ.get('SKYNAMO_INSTANCE_NAME')
	apiKey=os.environ.get('SKYNAMO_API_KEY')
	if instanceName==None or apiKey==None:
		updateEnvironmentVariablesFromJsonConfig()
		instanceName=os.environ.get('SKYNAMO_INSTANCE_NAME')
		apiKey=os.environ.get('SKYNAMO_API_KEY')
	print(apiKey)
	return {'x-api-client':instanceName,'x-api-key':apiKey,'accept':'application/json'}

class Write:
	def __init__(self,dataType:str,httpMethod:Literal['post','patch','put'],item:dict[str,Union[str,int,float,bool,list]]):
		self.dataType=dataType
		self.item=item
		self.httpMethod=httpMethod

class WriteError:
	def __init__(self,dataType:str,httpMethod:Literal['post','patch','put'],item:dict[str,Union[str,int,float,bool,list]],error:list[str]):
		self.dataType=dataType
		self.item=item
		self.httpMethod=httpMethod
		self.error=error

def makeWriteRequest(writeBatch:list[Write],errors:list[WriteError]):
	writeItems=[]
	for write in writeBatch:
		writeItems.append(write.item)
	#results=eval(f'requests.{writeBatch[0].httpMethod}(getApiBase()+"{writeBatch[0].dataType}",headers=getHeaders(),json=writeItems).json()')
	results=requests.post(getApiBase()+writeBatch[0].dataType,headers=getHeaders(),json=writeItems).json()
	if 'errors' in results:
		for error in results['errors']:
			errors.append(WriteError(writeBatch[0].dataType,writeBatch[0].httpMethod,writeItems[error['index']],error['detail'])) #type:ignore

def makeWrites(writes:list[Write]):
	writeBatchesGroupedByDataTypeAndHttpMethod=[]
	for write in writes:
		found=False
		for writeBatch in writeBatchesGroupedByDataTypeAndHttpMethod:
			if writeBatch[0].dataType==write.dataType and writeBatch[0].httpMethod==write.httpMethod:
				writeBatch.append(write)
				found=True
				break
		if not found:
			writeBatchesGroupedByDataTypeAndHttpMethod.append([write])
	subBatchesWithMaxSizeOf20:list[list[Write]]=[]
	for writeBatch in writeBatchesGroupedByDataTypeAndHttpMethod:
		for i in range(math.ceil(len(writeBatch)/20)):
			subBatchesWithMaxSizeOf20.append(writeBatch[i*20:i*20+20])
	return makeThreadedWrites(subBatchesWithMaxSizeOf20)

def makeThreadedWrites(subBatchesWithMaxSizeOf20:list[list[Write]]):
	threads=[]
	errors:list[WriteError]=[]
	for subBatch in subBatchesWithMaxSizeOf20:
		threads.append(threading.Thread(target=makeWriteRequest,args=(subBatch,errors)))
	for thread in threads:
		thread.start()
	for thread in threads:
		thread.join()
	return errors

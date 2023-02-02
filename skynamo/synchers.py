from .helpers import ensureFolderExists
import requests
from typing import Union,Literal
from .SkynamoAPI import getApiBase,getHeaders
import ujson,math,threading

def AddPageResultToExistingItemsAndReturnTotalItems(dataType:str,existingItems:dict,pageNr:int,pageSize:int,idField:str,filters:str,flags:list[str]=[]):
	print(f'Pagenr: {pageNr}')
	params:dict[str,Union[str,int]]={'page_number':pageNr,'page_size':pageSize}
	if filters!='':
		params['filters']=filters
	if flags!=[]:
		params['flags']=','.join(flags)
	jsonResponse=requests.get(getApiBase()+dataType,headers=getHeaders(),params=params).json()
	if 'message' in jsonResponse:
		if jsonResponse['message']=='Forbidden':
			raise Exception('Invalid region, instance name or api key')
	totalItems=0
	if 'page' in jsonResponse:
		totalItems=jsonResponse['page']['filtered_item_count']
	if 'data' in jsonResponse:
		data=jsonResponse['data']
		for item in data:
			id=item[idField]
			existingItems[str(id)]=item
	return totalItems

def addLatestRowVersionToExistingData(existingData:dict,existingItems:dict):
	latestRowVersion=0
	for item in existingItems.values():
		possibleVersionKeys=['row_version','version']
		for key in possibleVersionKeys:
			if key in item:
				rowVersion=item[key]
				if rowVersion>latestRowVersion:
					latestRowVersion=rowVersion
	existingData['lastRowVersion']=latestRowVersion

def SyncDataTypeFromSkynamoToLocalJsonFiles(dataType,fullSync=False,idField='id',syncFromLastRowVersion=False,flags:list[str]=[]):
	exceptionThatOccured=None
	print(f'Starting sync for {dataType}')
	pageSize=200
	totalItems=-1
	existingData={'lastPageNr':1,'items':{},'lastRowVersion':0}
	if not(fullSync):
		try:
			with open(f'skynamo-cache/{dataType}.json', "r") as read_file:
				existingData=ujson.load(read_file)
		except Exception as e:
			pass
	pageNr=1
	filters=''
	if syncFromLastRowVersion:
		rowVersion=existingData['lastRowVersion']
		filters=f'[\"greater_than(version,{rowVersion})\"]'
	else:
		pageNr=existingData['lastPageNr']
	existingItems=existingData['items']
	try:
			totalItems=AddPageResultToExistingItemsAndReturnTotalItems(dataType,existingItems,pageNr,pageSize,idField,filters,flags)
			pageNr=pageNr+1
			predictedNumberOfPages=math.ceil(totalItems/pageSize)
			while pageNr<=predictedNumberOfPages:
				pagesLeft=predictedNumberOfPages-pageNr + 1
				nrThreads=pagesLeft
				if nrThreads>20:
					nrThreads=20
				threads=[]
				for t in range(nrThreads):
					t=threading.Thread(target=AddPageResultToExistingItemsAndReturnTotalItems,args=(dataType,existingItems,pageNr+t,pageSize,idField,filters,flags))
					t.start()
					threads.append(t)
				for thread in threads:
					thread.join()
				pageNr=pageNr+nrThreads
	except Exception as e:
		exceptionThatOccured=e

	addLatestRowVersionToExistingData(existingData,existingItems)
	existingData['lastPageNr']=pageNr-1
	with open(f'skynamo-cache/{dataType}.json', "w") as write_file:
		print(f'updating cache for {dataType}')
		ujson.dump(existingData, write_file)
	if exceptionThatOccured!=None:
		raise exceptionThatOccured

def SyncDataTypesFromSkynamo(dataTypes:list[Literal['completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','formdefinitions','interactions']]=['completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','interactions']):
	ensureFolderExists('skynamo-cache')
	fullSyncDataTypes=['users','stocklevels','formdefinitions']
	versionedDataTypes=['customers','products','invoices']
	dataTypesWithCustomIds={'stocklevels':'product_id'}
	dataTypeFlags={'formdefinitions':['show_enums'],'orders':['show_nulls'],'creditrequests':['show_nulls'],'quotes':['show_nulls']}
	flags=[]
	for dataType in dataTypes:
		id='id'
		if dataType in dataTypesWithCustomIds:
			id=dataTypesWithCustomIds[dataType]
		fullSync=False
		if dataType in fullSyncDataTypes:
			fullSync=True
		syncFromLastRowVersion=False
		if dataType in versionedDataTypes:
			syncFromLastRowVersion=True
		if dataType in dataTypeFlags:
			flags=dataTypeFlags[dataType]
		SyncDataTypeFromSkynamoToLocalJsonFiles(dataType,fullSync,id,syncFromLastRowVersion,flags)
import json
from .skynamoDataClasses.StockLevel import StockLevel
from .skynamoDataClasses.Invoice import Invoice
from .skynamoDataClasses.User import User
from .synchers import SyncDataTypesFromSkynamo

from typing import Literal
from .skynamoDataClasses.Transaction import Transaction
from .skynamoDataClasses.Address import Address
from .helpers import getDateTimeObjectFromSkynamoDateTimeStr,getStringWithOnlyValidPythonVariableCharacters

def populateUserIdAndNameFromInteractionAndReturnFormIds(transaction:Transaction):
	interactionsJson={}
	with open(f'skynamo-cache/interactions.json', "r") as read_file:
		interactionsJson=json.load(read_file)
	interaction=interactionsJson['items'][str(transaction.interaction_id)]
	transaction.user_id=interaction['user_id']
	transaction.user_name=interaction['user_name']
	formIds=[]
	if 'completed_form_ids' in interaction:
		formIds=interaction['completed_form_ids']
	return formIds

def populateCustomPropsFromFormResults(transaction:Transaction,formIds:list[int]):
	formResultsJson={}
	with open(f'skynamo-cache/completedforms.json', "r") as read_file:
		formResultsJson=json.load(read_file)
	for id in formIds:
		formRes=formResultsJson['items'][str(id)]
		for customField in formRes['custom_fields']:
			customFieldId=customField['id']
			customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
			formId=formRes['form_id']
			customProp=f'f{formId}_c{customFieldId}_{customFieldName}'
			setTypeCorrectedCustomFieldValue(transaction,customField,customProp)

def getOrders():
	from skynamoInstanceDataClasses.Order import Order
	refreshJsonFilesLocallyIfOutdated(['orders','completedforms','interactions'])
	orders:list[Order]=getListOfObjectsFromJsonFile('skynamo-cache/orders.json',Order)
	for order in orders:
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(order)#type:ignore
		populateCustomPropsFromFormResults(order,formIds)#type:ignore
	return orders

def getCreditRequests():
	from skynamoInstanceDataClasses.CreditRequest import CreditRequest
	refreshJsonFilesLocallyIfOutdated(['creditrequests','completedforms','interactions'])
	creditRequests:list[CreditRequest] = getListOfObjectsFromJsonFile('skynamo-cache/creditrequests.json',CreditRequest)
	for creditRequest in creditRequests:
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(creditRequest)#type:ignore
		populateCustomPropsFromFormResults(creditRequest,formIds)#type:ignore
	return creditRequests

def getQuotes():
	from skynamoInstanceDataClasses.Quote import Quote
	refreshJsonFilesLocallyIfOutdated(['quotes','completedforms','interactions'])
	quotes:list[Quote]= getListOfObjectsFromJsonFile('skynamo-cache/quotes.json',Quote)
	for quote in quotes:
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(quote)#type:ignore
		populateCustomPropsFromFormResults(quote,formIds)#type:ignore
	return quotes

def getProducts():
	from skynamoInstanceDataClasses.Product import Product
	refreshJsonFilesLocallyIfOutdated(['products'])
	products:list[Product]= getListOfObjectsFromJsonFile('skynamo-cache/products.json',Product)
	return products

def getCustomers():
	from skynamoInstanceDataClasses.Customer import Customer
	refreshJsonFilesLocallyIfOutdated(['customers'])
	customers:list[Customer]= getListOfObjectsFromJsonFile('skynamo-cache/customers.json',Customer)
	return customers


def getInvoices():
	refreshJsonFilesLocallyIfOutdated(['invoices'])
	invoices:list[Invoice]=getListOfObjectsFromJsonFile('skynamo-cache/invoices.json',Invoice)
	return invoices

def getStockLevels():
	refreshJsonFilesLocallyIfOutdated(['stocklevels'])
	stockLevels= getListOfObjectsFromJsonFile('skynamo-cache/stocklevels.json',StockLevel)
	return stockLevels

def getFormResults(FormClass):
	refreshJsonFilesLocallyIfOutdated(['completedforms'])
	return getListOfObjectsFromJsonFile('skynamo-cache/completedforms.json',FormClass)

def getUsers():
	refreshJsonFilesLocallyIfOutdated(['users'])
	users:list[User]= getListOfObjectsFromJsonFile('skynamo-cache/users.json',User)
	return users


def setTypeCorrectedCustomFieldValue(item:object,customField:dict,customProp:str):
	## check if customProp is in _skippedCustomFields and skip if so
	if customProp in item._skippedCustomFields:#type:ignore
		return
	## check if customProp is a valid property of item
	if customProp not in item.__dict__:
		raise Exception(f"{customProp} is not a valid property of {type(item).__name__}. Rerun updateInstanceDataClasses.py to update this instance's data classes.")
	typeCorrectedCustomFieldValue=customField['value']
	if typeCorrectedCustomFieldValue=='':
		return # don't set empty values
	expectedPropType=item.__getattribute__('_customFieldPropTypes')[customProp]
	if expectedPropType=='int':
		typeCorrectedCustomFieldValue=int(typeCorrectedCustomFieldValue)
	elif expectedPropType=='float':
		typeCorrectedCustomFieldValue=float(typeCorrectedCustomFieldValue)
	elif expectedPropType=='datetime':
		typeCorrectedCustomFieldValue=getDateTimeObjectFromSkynamoDateTimeStr(typeCorrectedCustomFieldValue)
	elif expectedPropType=='Address':
		typeCorrectedCustomFieldValue=Address(typeCorrectedCustomFieldValue)
	elif expectedPropType[:4]=='list':
		stringAr=typeCorrectedCustomFieldValue.split(',')
		if expectedPropType[5:8]=='int':
			typeCorrectedCustomFieldValue=[]
			for i in range(len(stringAr)):
				typeCorrectedCustomFieldValue.append(int(stringAr[i]))
		else:
			typeCorrectedCustomFieldValue=stringAr
	setattr(item,customProp,typeCorrectedCustomFieldValue)

def getListOfObjectsFromJsonFile(jsonFile:str,DataClass):
	formIdToFilterOn=0
	if '_f' in DataClass.__name__:
		formIdToFilterOn=int(DataClass.__name__.split('_f')[-1])
	jsonDict={}
	with open(jsonFile, "r") as read_file:
		jsonDict=json.load(read_file)
	listOfObjects=[]
	for itemId in jsonDict['items']:
		item=jsonDict['items'][itemId]
		if formIdToFilterOn!=0:
			if item['form_id']!=formIdToFilterOn:
				continue
		obj=DataClass(item)
		if 'custom_fields' in item:
			for customField in item['custom_fields']:
				customFieldId=customField['id']
				customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
				customProp=f'c{customFieldId}_{customFieldName}'
				setTypeCorrectedCustomFieldValue(obj,customField,customProp)
		listOfObjects.append(obj)
	return listOfObjects

def refreshJsonFilesLocallyIfOutdated(dataTypes:list[Literal['completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','formdefinitions','interactions']]):
	import os
	import time
	nrSecondsToWaitBeforeRefreshing=300
	if os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')!=None:
		try:
			nrSecondsToWaitBeforeRefreshing=int(os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')) #type: ignore
		except:
			pass
	# if any datatype is outdated then refresh all but only once
	for dataType in dataTypes:
		if os.path.exists(f'skynamo-cache/{dataType}.json'):
			fileLastModifiedTime = os.path.getmtime(f'skynamo-cache/{dataType}.json')
			if time.time()-fileLastModifiedTime>nrSecondsToWaitBeforeRefreshing:
				SyncDataTypesFromSkynamo(dataTypes)
				break
		else:
			SyncDataTypesFromSkynamo(dataTypes)
			break
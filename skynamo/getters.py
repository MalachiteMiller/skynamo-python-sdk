import ujson
from .skynamoDataClasses.StockLevel import StockLevel
from .skynamoDataClasses.Invoice import Invoice
from .skynamoDataClasses.User import User
from .synchers import SyncDataTypesFromSkynamo

from typing import Literal
from .skynamoDataClasses.Transaction import Transaction
from .skynamoDataClasses.Address import Address
from .helpers import getDateTimeObjectFromSkynamoDateTimeStr,getStringWithOnlyValidPythonVariableCharacters

def populateUserIdAndNameFromInteractionAndReturnFormIds(transaction:Transaction,interactionsJson:dict):
	interaction=interactionsJson['items'][str(transaction.interaction_id)]
	transaction.user_id=interaction['user_id']
	transaction.user_name=interaction['user_name']
	formIds=[]
	if 'completed_form_ids' in interaction:
		formIds=interaction['completed_form_ids']
	return formIds

def populateCustomPropsFromFormResults(transaction:Transaction,formIds:list[int],completedForms:dict):
	for id in formIds:
		formRes=completedForms['items'][str(id)]
		for customField in formRes['custom_fields']:
			customFieldId=customField['id']
			customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
			formId=formRes['form_id']
			customProp=f'f{formId}_c{customFieldId}_{customFieldName}'
			setTypeCorrectedCustomFieldValue(transaction,customField,customProp)

def getTransactions(transactionClass,forceRefresh:bool):
	refreshJsonFilesLocallyIfOutdated([f'{transactionClass.__name__.lower()}s','completedforms','interactions'])#type:ignore
	interactionsJson={}
	with open(f'skynamo-cache/interactions.json', "r") as read_file:
		interactionsJson=ujson.load(read_file)
	refreshJsonFilesLocallyIfOutdated(['orders','completedforms','interactions'],forceRefresh)
	completedForms={}
	with open(f'skynamo-cache/completedforms.json', "r") as read_file:
		completedForms=ujson.load(read_file)
	transactions=getListOfObjectsFromJsonFile(f'skynamo-cache/{transactionClass.__name__.lower()}s.json',transactionClass)
	for i,transaction in enumerate(transactions):
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(transaction,interactionsJson)#type:ignore
		populateCustomPropsFromFormResults(transaction,formIds,completedForms)#type:ignore
	return transactions

def getOrders(forceRefresh=False):
	from skynamoInstanceDataClasses.Order import Order
	orders:list[Order]=getTransactions(Order,forceRefresh)
	return orders

def getCreditRequests(forceRefresh=False):
	from skynamoInstanceDataClasses.CreditRequest import CreditRequest
	creditRequests:list[CreditRequest]=getTransactions(CreditRequest,forceRefresh)
	return creditRequests

def getQuotes(forceRefresh=False):
	from skynamoInstanceDataClasses.Quote import Quote
	quotes:list[Quote]=getTransactions(Quote,forceRefresh)
	return quotes

def getProducts(forceRefresh=False):
	from skynamoInstanceDataClasses.Product import Product
	refreshJsonFilesLocallyIfOutdated(['products'],forceRefresh)
	products:list[Product]= getListOfObjectsFromJsonFile('skynamo-cache/products.json',Product)
	return products

def getCustomers(forceRefresh=False):
	from skynamoInstanceDataClasses.Customer import Customer
	refreshJsonFilesLocallyIfOutdated(['customers'],forceRefresh)
	customers:list[Customer]= getListOfObjectsFromJsonFile('skynamo-cache/customers.json',Customer)
	return customers


def getInvoices(forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated(['invoices'],forceRefresh)
	invoices:list[Invoice]=getListOfObjectsFromJsonFile('skynamo-cache/invoices.json',Invoice)
	return invoices

def getStockLevels(forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated(['stocklevels'],forceRefresh)
	stockLevels= getListOfObjectsFromJsonFile('skynamo-cache/stocklevels.json',StockLevel)
	return stockLevels

def getFormResults(FormClass,forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated(['completedforms'],forceRefresh)
	return getListOfObjectsFromJsonFile('skynamo-cache/completedforms.json',FormClass)

def getUsers(forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated(['users'],forceRefresh)
	users:list[User]= getListOfObjectsFromJsonFile('skynamo-cache/users.json',User)
	return users


def setTypeCorrectedCustomFieldValue(item:object,customField:dict,customProp:str):
	## check if customProp is in _skippedCustomFields and skip if so
	if customProp in item._skippedCustomFields:#type:ignore
		return
	## check if customProp is a valid property of item
	if customProp not in item.__dict__:
		raise Exception(f"{customProp} is not a valid property of {type(item).__name__}. Rerun updateInstanceDataClasses.py to update this instance's data classes.")
	if not 'value' in customField:
		return # don't set empty values
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
		jsonDict=ujson.load(read_file)
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

def refreshJsonFilesLocallyIfOutdated(dataTypes:list[Literal['completedforms','quotes','orders','creditrequests','users','stocklevels','customers','products','invoices','formdefinitions','interactions']],forceRefresh:bool=False):
	import os
	import time
	nrSecondsToWaitBeforeRefreshing=300
	if os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')!=None:
		try:
			nrSecondsToWaitBeforeRefreshing=int(os.environ.get('SKYNAMO_CACHE_REFRESH_INTERVAL')) #type: ignore
		except:
			pass

	for dataType in dataTypes:
		if os.path.exists(f'skynamo-cache/{dataType}.json'):
			fileLastModifiedTime = os.path.getmtime(f'skynamo-cache/{dataType}.json')
			if forceRefresh or time.time()-fileLastModifiedTime>nrSecondsToWaitBeforeRefreshing:
				SyncDataTypesFromSkynamo([dataType])
		else:
			SyncDataTypesFromSkynamo([dataType])
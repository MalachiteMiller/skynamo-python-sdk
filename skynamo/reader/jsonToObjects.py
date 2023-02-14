import ujson
from ..models.Transaction import Transaction
from ..models.Address import Address
from ..models.OrderUnit import OrderUnit
from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr,getStringWithOnlyValidPythonVariableCharacters
from typing import List

def populateUserIdAndNameFromInteractionAndReturnFormIds(transaction:Transaction,interactionsJson:dict):
	interaction=interactionsJson['items'][str(transaction.interaction_id)]
	transaction.user_id=interaction['user_id']
	transaction.user_name=interaction['user_name']
	formIds=[]
	if 'completed_form_ids' in interaction:
		formIds=interaction['completed_form_ids']
	return formIds

def populateCustomPropsFromFormResults(transaction:Transaction,formIds:List[int],completedForms:dict):
	for id in formIds:
		formRes=completedForms['items'][str(id)]
		for customField in formRes['custom_fields']:
			customFieldId=customField['id']
			customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
			formId=formRes['form_id']
			customProp=f'f{formId}_c{customFieldId}_{customFieldName}'
			setTypeCorrectedCustomFieldValue(transaction,customField,customProp)


def setTypeCorrectedCustomFieldValue(item:object,customField:dict,customProp:str):
	## check if customProp is a valid property of item
	if customProp not in item.__dict__:
		return
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
		adr=Address()
		adr.populateFromJsonValue(typeCorrectedCustomFieldValue)
		typeCorrectedCustomFieldValue=adr
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
import ujson
from ..models.Transaction import Transaction
from ..models.Address import Address
from ..shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr,getStringWithOnlyValidPythonVariableCharacters

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
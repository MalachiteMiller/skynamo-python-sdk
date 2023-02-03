from datetime import datetime
from ..SkynamoAPI import Write

def isBasicType(fieldValue):
	return isinstance(fieldValue,str) or isinstance(fieldValue,bool) or isinstance(fieldValue,int) or isinstance(fieldValue,float) or isinstance(fieldValue,list) or fieldValue==None

def getJsonReadyFieldValue(fieldValue):
	if isinstance(fieldValue,datetime):
		return fieldValue.strftime('%Y-%m-%dT%H:%M:%S')
	elif isBasicType(fieldValue)==False:
		return fieldValue.getJsonReadyValue()
	else:
		return fieldValue

def getCustomFieldIdIfFieldIsCustomField(fieldName:str):
	## return number if field matches pattern "c{number}_*"
	if fieldName[0]=='c' and fieldName[1:].split('_')[0].isdigit():
		return int(fieldName[1:].split('_')[0])
	else:
		return None

def addPatchedFieldToBodyIfAllowed(body:dict,fieldName:str,fieldValue,object:object):
	if fieldName in ['id','row_version','version','create_date','last_modified_time','tax']:
		raise Exception(f'Field {fieldName} cannot be patched')
	if fieldName not in object.__dict__:
		raise Exception(f'Field {fieldName} is not a valid {type(object).__name__} field')
	customFieldId=getCustomFieldIdIfFieldIsCustomField(fieldName)
	jsonReadyFieldValue=getJsonReadyFieldValue(fieldValue)
	if customFieldId!=None:
		if 'custom_fields' not in body:
			body['custom_fields']=[]
		body['custom_fields'].append({'id':customFieldId,'value':jsonReadyFieldValue})
	else:
		body[fieldName]=jsonReadyFieldValue

def getWriteObjectToPatchObject(object:object,fieldsToPatch:list[str]):
	body={'id':object.id}#type:ignore
	for fieldName in fieldsToPatch:
		fieldValue=object.__dict__[fieldName]
		if fieldValue==None:
			raise Exception(f'Error in field: {fieldName}. If a field has a value, the value cannot be removed (set to None).')
		addPatchedFieldToBodyIfAllowed(body,fieldName,object.__dict__[fieldName],object)
	import json
	print(json.dumps(body))
	return Write(type(object).__name__.lower()+'s', "patch", body)
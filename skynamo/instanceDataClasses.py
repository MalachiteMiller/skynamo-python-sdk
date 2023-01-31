from .SkynamoAPI import SyncDataTypesFromSkynamo
import json,os
from .helpers import ensureFolderExists,getStringWithOnlyValidPythonVariableCharacters

def deleteExistingInstanceDataClasses():
	## remove skynamoInstanceDataClasses subfolders and files
	if os.path.exists('skynamoInstanceDataClasses'):
		for root, dirs, files in os.walk('skynamoInstanceDataClasses', topdown=False):
			for name in files:
				os.remove(os.path.join(root, name))
			for name in dirs:
				os.rmdir(os.path.join(root, name))

def updateInstanceDataClasses():
	SyncDataTypesFromSkynamo(['formdefinitions'])
	ensureFolderExists('skynamoInstanceDataClasses')
	deleteExistingInstanceDataClasses()
	with open(f'skynamo-cache/formdefinitions.json', "r") as read_file:
		formsJson=json.load(read_file)
	for formDefId in formsJson['items']:
		formDef=formsJson['items'][formDefId]
		if formDef['active']==True:
			updateInstanceDataClassFromFormDef(formDef)

def updateInstanceDataClassFromFormDef(formDef):
	formId=formDef['id']
	formName=formDef['name']
	if formName in ['Dropbox','SkynamoServices']:
		return
	formType=formDef['type']
	customFields=formDef['custom_fields']
	baseClass='FormResult'
	instanceClassName=getStringWithOnlyValidPythonVariableCharacters(formName)+f'_f{formId}'
	formPrefix=''
	if formType in ['Order','CreditRequest','Quote']:
		formPrefix=f'f{formId}_'
		baseClass='Transaction'
		instanceClassName=formType
	elif formId==-3:
		baseClass='Product'
		instanceClassName='Product'
	elif formId==-1:
		baseClass='Customer'
		instanceClassName='Customer'
	
	with open(f'skynamo/skynamoDataClasses/{baseClass}.py', "r") as read_file:
		dataClass=read_file.read()
		dataClass=dataClass.replace(f'class {baseClass}:',f'class {instanceClassName}:')
		skippedCustomFieldTypes=['Images Field','Signature Field','Sketch Field','Divider Field','Label Field']
		with open(f'skynamoInstanceDataClasses/{instanceClassName}.py', "w") as write_file:
			write_file.write(dataClass)
			customFieldPropTypes={}
			skippedCustomFields=[]
			for customField in customFields:
				customFieldType=customField['type']
				customFieldId=customField['id']
				customFieldName=getStringWithOnlyValidPythonVariableCharacters(customField['name'])
				customPropName=f'{formPrefix}c{customFieldId}_{customFieldName}'
				if customFieldType in skippedCustomFieldTypes:
					skippedCustomFields.append(customPropName)
					continue
				
				propType='str'
				if customFieldType=='Text Field':
					propType='str'
				elif customFieldType=='Number Field':
					propType='float'
				elif customFieldType=='Date Time Field':
					propType='datetime'
				elif customFieldType=='Single Value Enumeration Field':
					commaSeparatedOptions=getCommaSeperatedEnums(customField['enumeration_values'])
					propType=f'Literal["{commaSeparatedOptions}"]'
				elif customFieldType=='Multi Value Enumeration Field':
					commaSeparatedOptions=getCommaSeperatedEnums(customField['enumeration_values'])
					propType=f'list[Literal["{commaSeparatedOptions}"]]'
				elif customFieldType=='Single Value Hierarchical Enumeration Field':
					commaSeparatedOptions=getCommaSeperatedEnumsForNestedEnums(customField['enumeration_values'])
					propType=f'Literal["{commaSeparatedOptions}"]'
				elif customFieldType=='Multi Value Hierarchical Enumeration Field':
					commaSeparatedOptions=getCommaSeperatedEnumsForNestedEnums(customField['enumeration_values'])
					propType=f'list[Literal["{commaSeparatedOptions}"]]'
				elif customFieldType=='Address Field':
					propType='Address'
				elif customFieldType=='Single Value Lookup Entity Field':
					propType='int'
				elif customFieldType=='Multi Value Lookup Entity Field':
					propType='list[int]'
				defaultValue='None'
				
				
				customFieldPropTypes[customPropName]=propType
				write_file.write(f'\t\tself.{customPropName}:Union[{propType},None]={defaultValue}\r')
			write_file.write(f'\t\tself._customFieldPropTypes:dict[str,str]={customFieldPropTypes}\r')
			write_file.write(f'\t\tself._skippedCustomFields:list[str]={skippedCustomFields}\r')

def getCommaSeperatedEnums(enumerationValues:list[dict]):
	commaSeparatedOptions=''
	for enum in enumerationValues:
		commaSeparatedOptions+=f'{enum["label"]},'
	return commaSeparatedOptions[:-1]

def getCommaSeperatedEnumsForNestedEnums(enumValues:list[dict]):
	commaSeparatedOptions=''
	parentToChildEnumValues={}
	for enum in enumValues:
		if 'parent_id' not in enum:
			parentToChildEnumValues[enum['id']]={'label':enum['label'],'children':[]}
		else:
			parentToChildEnumValues[enum['parent_id']]['children'].append(enum)
	for parentEnumId in parentToChildEnumValues:
		for childEnum in parentToChildEnumValues[parentEnumId]['children']:
			commaSeparatedOptions+=f'{parentToChildEnumValues[parentEnumId]["label"]} - {childEnum["label"]},'
	return commaSeparatedOptions[:-1]


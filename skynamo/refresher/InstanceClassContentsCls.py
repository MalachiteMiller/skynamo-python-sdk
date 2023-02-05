from ..shared.helpers import writeToInstanceSpecificFile
import os
from .refreshHelpers import getNameOfModelClassOnWhichToAddCustomFieldFromFormDefinition,isCustomForm
from .CustomFieldArg import getListCustomFieldArgs,CustomFieldArg

def getStringContentOfClassInMainFolder(className:str):
	if className[-3:]!='.py':
		className+='.py'
	sharedPath = os.path.dirname(os.path.realpath(__file__)).replace('\\','/')
	mainPath=sharedPath.replace('/shared','/main')
	with open(f'{mainPath}/{className}', "r") as read_file:
		return read_file.read()

class InstanceClassContents:
	def __init__(self):
		self.writerContent=getStringContentOfClassInMainFolder('Writer')
		self.readerContent=getStringContentOfClassInMainFolder('Reader')
		self.orderContent=getStringContentOfClassInMainFolder('Orders')
		self.quoteContent=getStringContentOfClassInMainFolder('Quotes')
		self.creditrequestContent=getStringContentOfClassInMainFolder('CreditRequests')
		self.productContent=getStringContentOfClassInMainFolder('Products')
		self.customerContent=getStringContentOfClassInMainFolder('Customers')

		self.__customFormBaseContent=getStringContentOfClassInMainFolder('CustomForm')
		self.customFormsContent={}

	def write(self):
		writeToInstanceSpecificFile('Writer',self.writerContent)
		writeToInstanceSpecificFile('Reader',self.readerContent)
		writeToInstanceSpecificFile('Orders',self.orderContent)
		writeToInstanceSpecificFile('Quotes',self.quoteContent)
		writeToInstanceSpecificFile('CreditRequests',self.creditrequestContent)
		writeToInstanceSpecificFile('Products',self.productContent)
		writeToInstanceSpecificFile('Customers',self.customerContent)
		for customFormName,customFormContent in self.customFormsContent.items():
			writeToInstanceSpecificFile(customFormName,customFormContent)

	def addFormDefinitionToRelevantClassContents(self,formDef:dict):
		formId=formDef['id']
		formName=formDef['name']
		if formName in ['Dropbox','SkynamoServices']:
			return
		customFieldArgs=getListCustomFieldArgs(formDef)
		modelClassName=getNameOfModelClassOnWhichToAddCustomFieldFromFormDefinition(formDef)
		self.__addCustomFieldsToRelevantModelClassContents(customFieldArgs,modelClassName,formId)
		self.__addCustomFieldsToWriterIfApplicable(customFieldArgs,modelClassName)
		self.__addCustomFormGetMethodsToReader(modelClassName)

	def __addCustomFieldsToRelevantModelClassContents(self,customFieldArgs:list[CustomFieldArg],modelClassName:str,formId:str):
		modelClassString=self.__customFormBaseContent.replace(f'class CustomForm:',f'class {modelClassName}:')
		if not(isCustomForm(modelClassName)):
			modelClassString=self.__getattribute__(f'{modelClassName.lower()}Content')
		customFieldArgsWithPropTypes={}
		for customFieldArg in customFieldArgs:
			modelClassString+=f'\t\tself.{customFieldArg.argName}:Union[{customFieldArg.argType},None]=None\r'
			customFieldArgsWithPropTypes[customFieldArg.argName]=customFieldArg.argType
		modelClassString+=f'\t\tself._{formId}_customFieldPropTypes:dict[str,str]={customFieldArgsWithPropTypes}\r'

	def __addCustomFieldsToWriterIfApplicable(self,customFieldArgs:list[CustomFieldArg],modelClassName:str):
		if not(isCustomForm(modelClassName)):
			requiredCustomFieldsArgsAsString=[]
			optionalCustomFieldsArgsAsString=[]
			for customFieldArg in customFieldArgs:
				if customFieldArg.required:
					requiredCustomFieldsArgsAsString.append(f'{customFieldArg.argName}:{customFieldArg.argType}')
				else:
					optionalCustomFieldsArgsAsString.append(f'{customFieldArg.argName}:Union[{customFieldArg.argType},None]=None')
			placeHolder=f'##|required{modelClassName}CustomFields|##'
			self.writerContent=self.writerContent.replace(placeHolder,','.join(requiredCustomFieldsArgsAsString)+placeHolder)
			placeHolder=f'##|optional{modelClassName}CustomFields|##'
			self.writerContent=self.writerContent.replace(placeHolder,','.join(optionalCustomFieldsArgsAsString)+placeHolder)

	def __addCustomFormGetMethodsToReader(self,modelClassName:str):
		if isCustomForm(modelClassName):
			importString=f'from .{modelClassName} import {modelClassName}\r'
			importPlaceHolder='##|customImports|##'
			self.readerContent.replace(importPlaceHolder,importString+importPlaceHolder)
			getMethodString=f'\t\tdef get{modelClassName}(self,forceRefresh=False):\r'
			getMethodString+=f'\t\t\trefreshJsonFilesLocallyIfOutdated(["completedforms"],forceRefresh)\r'
			getMethodString+=f'\t\t\tresult:list[{modelClassName}]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation("completedforms"),{modelClassName})\r'
			getMethodString+=f'\t\t\treturn result\r'
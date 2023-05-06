import os,json
from datetime import datetime

def ensureFolderExists(folderPath):
	if not os.path.exists(folderPath):
		os.makedirs(folderPath)


def updateEnvironmentVariablesFromJsonConfig(selected_key: str = None):
	if selected_key is None:
		selected_key = 'SKYNAMO_API_KEY'
	with open('skynamo-config.json', "r") as read_file:
		config=json.load(read_file)
		os.environ['SKYNAMO_API_KEY']=config[selected_key]
		os.environ['SKYNAMO_INSTANCE_NAME']=config['SKYNAMO_INSTANCE_NAME']
		os.environ['SKYNAMO_REGION']=config['SKYNAMO_REGION']
		if 'REQUESTS_TIMEOUT' in config:
			os.environ['REQUESTS_TIMEOUT']=str(config['REQUESTS_TIMEOUT'])
		else:
			os.environ['REQUESTS_TIMEOUT']='300'
		if 'SKYNAMO_CACHE_REFRESH_INTERVAL' in config:
			os.environ['SKYNAMO_CACHE_REFRESH_INTERVAL']=str(config['SKYNAMO_CACHE_REFRESH_INTERVAL'])
		if 'SKYNAMO_GMAIL_SENDER' in config:
			os.environ['SKYNAMO_GMAIL_SENDER']=config['SKYNAMO_GMAIL_SENDER']
		if 'SKYNAMO_GMAIL_PASSWORD' in config:
			os.environ['SKYNAMO_GMAIL_PASSWORD']=config['SKYNAMO_GMAIL_PASSWORD']

def getDateTimeObjectFromSkynamoDateTimeStr(skynamoDateTimeStr:str):
	dateTimeStrWithoutMicroseconds=skynamoDateTimeStr[:19]+skynamoDateTimeStr[-6:]
	return datetime.strptime(dateTimeStrWithoutMicroseconds, "%Y-%m-%dT%H:%M:%S%z")

def getStringWithOnlyValidPythonVariableCharacters(string:str):
	allowedChars='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_'
	newString=''
	for char in string:
		if char in allowedChars:
			newString+=char
		else:
			newString+='_'
	if newString[0] in '0123456789':
		newString='_'+newString
	##remove non-utf8 characters
	newString=newString.encode('ascii', 'ignore').decode('ascii')
	return newString

def getPathRelativeToSkynamoDataFolder(relativeFilePath:str):
	if relativeFilePath[0]=='/':
		relativeFilePath=relativeFilePath[1:]
	return f'skynamo_data/{relativeFilePath}'

def clearInstanceSpecificFolder(relativeFolderPath:str):
	finalFolderPath=getPathRelativeToSkynamoDataFolder(relativeFolderPath)
	if os.path.exists(finalFolderPath):
		for file in os.listdir(finalFolderPath):
			os.remove(os.path.join(finalFolderPath, file))

def writeToInstanceSpecificFile(relativeFilePath:str,stringContent:str):
	finalFilePath=getPathRelativeToSkynamoDataFolder(relativeFilePath)
	with open(finalFilePath, "w") as write_file:
		write_file.write(stringContent)
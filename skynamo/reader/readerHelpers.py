def getCustomFieldWithName(skynamoObject,name:str):
	nameInProps=name.replace(' ','_')
	## if prop starts with c and ends with f'_{nameInProps}
	for prop in skynamoObject.__dict__:
		if prop[0] in ['c','f'] and f'_{nameInProps}'==prop[-len(nameInProps)-1:]:
			return skynamoObject.__dict__[prop]
	return None
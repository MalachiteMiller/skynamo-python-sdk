class OrderUnit:
	def __init__(self,name:str='',multiplier:int=1,active:bool=True):
		self.id=None
		self.name=name
		self.multiplier=multiplier
		self.active=active
	def populateFromJsonValue(self,jsonValue:dict):
		self.id=jsonValue['id']
		self.name=jsonValue['name']
		self.multiplier=jsonValue['multiplier']
		self.active=jsonValue['active']
	def getJsonReadyValue(self):
		return self.__dict__
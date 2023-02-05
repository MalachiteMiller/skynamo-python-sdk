class OrderUnit:
	def __init__(self,json:dict={}):
		self.id:int=json['id']
		self.name:str=json['name']
		self.multiplier:int=json['multiplier']
		self.active:bool=json['active']
	def getJsonReadyValue(self):
		return self.__dict__
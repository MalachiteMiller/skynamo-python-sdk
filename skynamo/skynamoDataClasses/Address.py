class Address:
	def __init__(self,addressString:str=''):

		self.street:str=''
		self.city:str=''
		self.state:str=''
		self.zip:str=''
		
		
		ar=addressString.split('\n')
		indexToKey={0:'street',1:'city',2:'state',3:'zip'}
		for i in range(0,4):
			if i<len(ar):
				self.__dict__[indexToKey[i]]=ar[i]

	def getJsonReadyValue(self):
		return f'{self.street}\n{self.city}\n{self.state}\n{self.zip}'
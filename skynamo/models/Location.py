class Location:
	def __init__(self,latitude:float,longitude:float,accuracy:float=0,is_approximate:bool=False):
		self.latitude:float=latitude
		self.longitude:float=longitude
		self.accuracy=accuracy
		self.is_approximate=is_approximate

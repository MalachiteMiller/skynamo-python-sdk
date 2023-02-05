from typing import Literal
class WriteError:
	def __init__(self,dataType:str,httpMethod:Literal['post','patch','put'],itemOrId:list,error:list[str]):
		self.dataType=dataType
		self.itemOrId=itemOrId
		self.httpMethod=httpMethod
		self.error=error
from typing import Union,Literal
from datetime import datetime
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.write.writeHelpers import getWriteObjectToPatchObject
from skynamo.skynamoDataClasses.Address import Address
from skynamo.SkynamoAPI import Write

class OrderUnit:
	def __init__(self,json:dict={}):
		self.id:int=json['id']
		self.name:str=json['name']
		self.multiplier:int=json['multiplier']
		self.active:bool=json['active']

class Product:
	def getWriteObjectToPatchProduct(self,fieldsToPatch:list[str]):
		return getWriteObjectToPatchObject(self,fieldsToPatch)

	def __init__(self,json:dict={}):
		self.id:str=json['id']
		self.row_version:int=json['row_version']
		self.code:str=json['code']
		self.name:str=json['name']
		self.active:bool=json['active']
		self.order_units:list[OrderUnit]=[]
		for order_unit in json['order_units']:
			self.order_units.append(OrderUnit(order_unit))
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])

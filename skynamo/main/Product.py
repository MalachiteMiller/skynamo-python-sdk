from typing import Union,Literal,List,Dict
from datetime import datetime
from skynamo.shared.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.models.Address import Address
from skynamo.models.OrderUnit import OrderUnit
from skynamo.reader.readerHelpers import getCustomFieldWithName

class Product:
	def getCustomFieldWithName(self,name:str):
		return getCustomFieldWithName(self,name)
	def __init__(self,json:dict={}):
		self.id:str=json['id']
		self.row_version:int=json['row_version']
		self.code:str=json['code']
		self.name:str=json['name']
		self.active:bool=json['active']
		self.order_units:List[OrderUnit]=[]
		for order_unit in json['order_units']:
			id=None
			if 'id' in order_unit:
				id=order_unit['id']
			self.order_units.append(OrderUnit(order_unit['name'],order_unit['multiplier'],id=id))
			if 'active' in order_unit:
				self.order_units[-1].active=order_unit['active']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])

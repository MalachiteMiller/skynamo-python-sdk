from datetime import datetime
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from typing import Union
from ..SkynamoAPI import Write

class StockLevel:
	def __init__(self,json:dict):
		self.product_id:int=json['product_id']
		self.product_code:str=json['product_code']
		self.product_name:str=json['product_name']
		self.order_unit_id:int=json['order_unit_id']
		self.order_unit_name:str=json['order_unit_name']
		self.warehouse_id:int=0
		if 'warehouse_id' in json:
			self.warehouse_id:int=json['warehouse_id']
		self.warehouse_name:str='Null warehouse'
		if 'warehouse_name' in json:
			self.warehouse_name:str=json['warehouse_name']
		self.level:int=json['level']
		self.label:Union[None,str]=None
		if 'label' in json:
			self.label:Union[None,str]=json['label']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])

def addWarehouseAndLabelIfPresent(item:dict,warehouse_id:int,warehouse_name:str,label:Union[None,str]):
	if warehouse_id:
		item['warehouse_id'] = warehouse_id
	elif warehouse_name!='Null warehouse':
		item['warehouse_name'] = warehouse_name
	if label:
		item['label'] = label

def getStockLevelPutUsingProductId(productId:int,level:int,warehouse_id:int=0,warehouse_name:str='Null warehouse',label:Union[None,str]=None):
	item={'product_id': productId, 'level': level}
	addWarehouseAndLabelIfPresent(item,warehouse_id,warehouse_name,label)
	return Write("stocklevels", "put", item)#type:ignore

def getStockLevelPutUsingProductCodeAndOrderUnitId(productCode:str,order_unit_id,level:int,warehouse_id:int=0,warehouse_name:str='Null warehouse',label:Union[None,str]=None):
	item={'product_code': productCode, 'order_unit_id': order_unit_id, 'level': level}
	addWarehouseAndLabelIfPresent(item,warehouse_id,warehouse_name,label)
	return Write("stocklevel", "put", item)

def getStockLevelPutUsingProductCodeAndOrderUnitName(productCode:str,order_unit_name:str,level:int,warehouse_id:int=0,warehouse_name:str='Null warehouse',label:Union[None,str]=None):
	item={'product_code': productCode, 'order_unit_name': order_unit_name, 'level': level}
	addWarehouseAndLabelIfPresent(item,warehouse_id,warehouse_name,label)
	return Write("stocklevels", "put", item)
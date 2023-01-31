from typing import Union,Literal
from datetime import datetime
from skynamo.skynamoDataClasses.Address import Address
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class TransactionItem:
	def __init__(self,json:dict):
		self.product_code:str=json['product_code']
		self.product_name:str=json['product_name']
		self.quantity:float=json['quantity']
		self.unit_price:float=json['unit_price']
		self.list_price:float=json['list_price']
		self.order_unit_name:str=json['order_unit_name']
		self.tax_rate_value:Union[float,None]=json['tax_rate_value']
		self.tax_rate_id:Union[int,None]=json['tax_rate_id']

class Transaction:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.customer_name:str=json['customer_name']
		self.reference:Union[str,None]=json['reference']
		self.interaction_id:int=json['interaction_id']
		self.discount_percentage:float=json['discount']
		self.discount_amount:float=json['discount_amount']
		self.total_amount:float=json['total_amount']
		self.prices_include_vat:Union[bool,None]=json['prices_include_vat']
		self.warehouse_id:Union[int,None]=json['warehouse_id']
		self.warehouse_name:Union[str,None]=json['warehouse_name']
		self.email_recipients:Union[str,None]=json['email_recipients']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		self.items:list[TransactionItem]=[]
		for item in json['items']:
			self.items.append(TransactionItem(item))

		## the following properties are populated from completed forms after the object is created:
		self.user_id:int=0
		self.user_name:str=''


from typing import Literal,Union
from datetime import datetime
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class InvoiceItem:
	def __init__(self,json:dict={}):
		self.product_id:int=json['product_id']
		self.product_code:str=json['product_code']
		self.quantity:float=json['quantity']
		self.totalLineValue:float=json['value']
		self.tax_amount:Union[None,float]=None
		if 'tax_amount' in json:
			self.tax_amount=json['tax_amount']

class Invoice:
	def __init__(self,json:dict={}):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.reference:str=json['reference']
		self.row_version:int=json['row_version']
		self.last_modified_time:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['last_modified_time'])
		self.status:Union[None,Literal['Draft','Authorized','Delivered','Outstanding','Paid','Deleted']]=None
		if 'status' in json:
			self.status=json['status']
		self.due_date:Union[None,datetime]=None
		if 'due_date' in json:
			self.due_date=getDateTimeObjectFromSkynamoDateTimeStr(json['due_date'])
		self.external_id:Union[None,str]=None
		if 'external_id' in json:
			self.external_id=json['external_id']
		self.tax_inclusion:Union[None,Literal['Included','Excluded']]=None
		if 'tax_inclusion' in json:
			self.tax_inclusion=json['tax_inclusion']
		self.total_tax_amount:Union[None,float]=None
		if 'tax' in json:
			self.total_tax_amount=json['tax']
		self.outstanding_balance:Union[None,float]=None
		if 'outstanding_balance' in json:
			self.outstanding_balance=json['outstanding_balance']
		self.items:list[InvoiceItem]=[]
		for item in json['items']:
			self.items.append(InvoiceItem(item))
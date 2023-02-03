from typing import Literal,Union
from datetime import datetime
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.write.writeHelpers import getWriteObjectToPatchObject

class InvoiceItem:
	def __init__(self,product_code:str,quantity:float,totalLineValue:float,tax_amount:Union[None,float]=None,product_id:Union[None,int]=None):
		self.product_id=product_id
		self.product_code:str=product_code
		self.quantity:float=quantity
		self.totalLineValue:float=totalLineValue
		self.tax_amount:Union[None,float]=tax_amount

	def getJsonReadyValue(self):
		res={
			'product_id':self.product_id,
			'product_code':self.product_code,
			'quantity':self.quantity,
			'value':self.totalLineValue
		}
		if self.tax_amount != None:
			res['tax_amount']=self.tax_amount
		return res

class Invoice:
	def getWriteObjectToUpdateInvoice(self,fieldsToUpdate:list[str]):
		return getWriteObjectToPatchObject(self,fieldsToUpdate)

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
			inputToInvoiceItem={'product_id':item['product_id'],'product_code':item['product_code'],'quantity':item['quantity'],'totalLineValue':item['value']}
			if 'tax_amount' in item:
				inputToInvoiceItem['tax_amount']=item['tax_amount']
			self.items.append(InvoiceItem(**inputToInvoiceItem))
from typing import Union,Literal
from datetime import datetime
from skynamo.skynamoDataClasses.Address import Address
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr

class FormResult:
	def __init__(self,json:dict):
		self.id:int=json['id']
		self.date:datetime=getDateTimeObjectFromSkynamoDateTimeStr(json['date'])
		self.customer_id:int=json['customer_id']
		self.customer_code:str=json['customer_code']
		self.customer_name:str=json['customer_name']
		self.user_id:int=json['user_id']
		self.user_name:str=json['user_name']
		self.interaction_id:int=json['interaction_id']
		self.form_id:int=json['form_id']
		self.form_name:str=json['form_name']

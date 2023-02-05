from typing import Union,Literal
from datetime import datetime
from skynamo.skynamoDataClasses.Address import Address
from skynamo.helpers import getDateTimeObjectFromSkynamoDateTimeStr
from skynamo.models.CustomFormBase import CustomFormBase

class CustomForm(CustomFormBase):
	def __init__(self,json:dict):
		super().__init__(json)

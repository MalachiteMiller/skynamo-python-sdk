from typing import Literal

class CustomFieldsToCreate:
	def __init__(self):
		self.fields_to_add=[]
		self.customerFieldNamesAdded=set()
		self.productFieldNamesAdded=set()
##fieldtypes=Text, Number, SingleSelect, MultiSelect, NestedSingleSelect, NestedMultiSelect, Address, UserSingleSelect, UserMultiSelect
	def addCustomerCustomField(self,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		if name in self.customerFieldNamesAdded:
			return
		self.fields_to_add.append({'name':name,'type':type,'form_id':-1})
		self.customerFieldNamesAdded.add(name)
	def addProductCustomField(self,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		if name in self.productFieldNamesAdded:
			return
		self.fields_to_add.append({'name':name,'type':type,'form_id':-3})
		self.productFieldNamesAdded.add(name)
	def addFormCustomField(self,formId:int,name:str,type:Literal['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address']):
		self.fields_to_add.append({'name':name,'type':type,'form_id':formId})
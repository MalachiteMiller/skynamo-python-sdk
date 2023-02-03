from typing import Union
from skynamo.SkynamoAPI import Write

def getCreateCustomerWriteObject(code:str,name:str,active:bool=True,latitude=0,longitude=0,price_list_id:Union[int,None]=None,price_list_name:Union[str,None]=None,assigned_users:list[int]=[],default_discount:float=0.0,default_warehouse_id:Union[int,None]=None,default_warehouse_name:Union[str,None]=None):
	body={'code': code, 'name': name,'active':active}
	if latitude!=0 or longitude!=0:
		body['location']={'latitude':latitude,'longitude':longitude}
	if price_list_id!=None:
		body['price_list_id']=price_list_id
	elif price_list_name!=None:
		body['price_list_name']=price_list_name
	if len(assigned_users)>0:
		body['assigned_users']=assigned_users
	if default_discount!=0.0:
		body['default_discount']=default_discount
	if default_warehouse_id!=None:
		body['default_warehouse_id']=default_warehouse_id
	elif default_warehouse_name!=None:
		body['default_warehouse_name']=default_warehouse_name
	return Write("customers", "post", body)

def getCreateProductWriteObject(code:str,name:str,unit_name:str='Unit',active:bool=True):
	body={'code': code, 'name': name,'active':active,'order_units':[{'name':unit_name,'multiplier':1}]}
	return Write("products", "post", body)



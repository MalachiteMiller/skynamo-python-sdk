from typing import Union,Literal
from skynamo.SkynamoAPI import Write
from datetime import datetime
from ..skynamoDataClasses.Invoice import InvoiceItem

def getCreateInvoiceUsingCustomerAndProductCodesWriteObject(date:datetime,customer_code:str,invoiceItems:list[InvoiceItem],reference='',status:Union[None,Literal['Draft','Authorized','Delivered','Outstanding','Paid','Deleted']]=None,due_date:Union[None,datetime]=None,tax_inclusion:Union[None,Literal['Included','Excluded']]=None,outstanding_balance:Union[None,float]=None):
	body={'date': date.strftime('%Y-%m-%dT%H:%M:%S'), 'customer_code': customer_code,'items':[]}
	for item in invoiceItems:
		body['items'].append({'product_code':item.product_code,'quantity':item.quantity,'totalLineValue':item.totalLineValue})
		if item.tax_amount!=None:
			body['items'][-1]['tax_amount']=item.tax_amount
	if reference!='':
		body['reference']=reference
	if status!=None:
		body['status']=status
	if due_date!=None:
		body['due_date']=due_date.strftime('%Y-%m-%dT%H:%M:%S')
	if tax_inclusion!=None:
		body['tax_inclusion']=tax_inclusion
	if outstanding_balance!=None:
		body['outstanding_balance']=outstanding_balance
	return Write("invoices", "post", body)


def getCreateScheduledVisitWriteObject(user_name:str,customer_code:str,visit_date_and_time_start:datetime,visit_date_and_time_end:datetime=None):#type:ignore
	body:dict[str,Union[str,bool]]={'user_name': user_name, 'customer_code': customer_code,'due_date':visit_date_and_time_start.strftime('%Y-%m-%dT%H:%M:%S')}
	if visit_date_and_time_end!=None:
		body['end_time']=visit_date_and_time_end.strftime('%Y-%m-%dT%H:%M:%S')
	else:
		body['all_day']=True
	return Write("scheduled_visits", "post", body)
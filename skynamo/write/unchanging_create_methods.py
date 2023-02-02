from typing import Union
from skynamo.SkynamoAPI import Write
from datetime import datetime


def getCreateScheduledVisitWriteObject(user_name:str,customer_code:str,visit_date_and_time_start:datetime,visit_date_and_time_end:datetime=None):#type:ignore
	body:dict[str,Union[str,bool]]={'user_name': user_name, 'customer_code': customer_code,'due_date':visit_date_and_time_start.strftime('%Y-%m-%dT%H:%M:%S')}
	if visit_date_and_time_end!=None:
		body['end_time']=visit_date_and_time_end.strftime('%Y-%m-%dT%H:%M:%S')
	else:
		body['all_day']=True
	return Write("scheduled_visits", "post", body)
# skynamo python SDK

## Overview
This package is a python SDK for skynamo public API. It allows you to pull data from your skynamo instance and update data in your skynamo instance. Some of the features include:
- Extending your instance's data classes with their respective custom fields. This allows you to use your IDE's autocomplete feature to easily access your custom fields.
- Pulling data from your skynamo instance and caching it locally to speed up subsequent calls and prevent hitting the skynamo API rate limit.
- Updating data in your skynamo instance using write batches to speed up the process and to prevent hitting the skynamo API rate limit.
- Saving raw or processed (e.g with filters or by combining different data types) skynamo data in csv files, which can be usefull for reporting.
- Sending emails using your gmail account.

## Requirements
- Python 3.6 or higher installed on your machine
- pip installed on your machine

## Installation
Run the following command in your terminal to install the skynamo python SDK:
```bash
pip install skynamo@git+https://github.com/skynamo/skynamo-python-sdk.git -I
```

If you are planning on sending emails you also need to install the following python packages:
- email
- smtplib

## Setup
Add skynamo-config.json in the root directory of your repository with the following information:
```json
{
	"SKYNAMO_INSTANCE_NAME":"coolestcompanyever",
	"SKYNAMO_REGION":"za",
	"SKYNAMO_API_KEY":"a3csg###########",
	"SKYNAMO_CACHE_REFRESH_INTERVAL": 300,
	"SKYNAMO_GMAIL_SENDER":"me@coolestcompanyever@gmail.com",
	"SKYNAMO_GMAIL_PASSWORD":"qg3gs###########",
}
```
- Instance name and region can be found in your skynamo instance url. For example, if your instance url is https://coolestcompanyever.za.skynamo.me, then your instance name is coolestcompanyever and your region is za (only other region is uk).
- Api key can be found by going to your skynamo instance, clicking on the settings icon in the top right corner, clicking on 'Integration tokens' (in left panel) and clicking on the "Add access token"
- Cache refresh interval is the number of seconds between cache refreshes. This does not need to be in the json file. If not specified, the default value is 300 seconds.
- Gmail sender and password can be used to send emails. Sender is the email address that will be used to send the emails and password is the google app password for that email address. Note the app password is not the same as your normal password and can be created by going to https://myaccount.google.com/apppasswords

## Creating your instance's data classes
```python
from skynamo import updateInstanceDataClasses

updateInstanceDataClasses()
```
This creates files in skynamoInstanceDataClasses folder with file containing python classes. Each class represents a data model that can be customized using skynamo's forms.

## Pulling data from your skynamo instance
```python
from skynamo import getCreditRequests, getCustomers, getOrders, getProducts, getQuotes, getFormResults, getInvoices, getStockLevels

creditRequests=getCreditRequests()
customers=getCustomers()
orders=getOrders()
quotes=getQuotes()
products=getProducts()
invoices=getInvoices()
stockLevels=getStockLevels()

from skynamoInstanceDataClasses import My_Custom_Form_f23
formResults=getFormResults(My_Custom_Form_f23)
```

## Updating data in your skynamo instance
To speed up any puts, posts or patches to your skynamo instance, this package creates write batches which it runs in parallel. To make any puts, posts or patches you need to build up a list of write objects and give the list to the 'makeWrites' method as shown below:
```python
from skynamo import makeWrites,getStockLevelPutUsingProductCodeAndOrderUnitName

stockLevelUpdate1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 1)
stockLevelUpdate2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 1)
listOfErrors=makeWrites([stockLevelUpdate1,stockLevelUpdate2]) #listOfErrors will be empty if all writes were successful
```

## Examples
Look in the tests folder for basic examples of how to use the package.
Look in this examples folder for some examples of more advanced usage.

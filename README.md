# skynamo python SDK
## Installation
pip install skynamo @ git+https://github.com/skynamo/skynamo-python-sdk.git
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
- Instance name and region can be found in your skynamo instance url. For example, if your instance url is https://coolestcompanyever.za.skynamo.me, then your instance name is coolestcompanyever and your region is za.
- Api key can be found by going to your skynamo instance, clicking on the settings icon in the top right corner, clicking on 'Integration tokens' (in left panel) and clicking on the "Add access token"
- Cache refresh interval is the number of seconds between cache refreshes. This does not need to be in the json file. If not specified, the default value is 300 seconds.
- Gmail sender and password can be used to send emails. Sender is the email address that will be used to send the emails and password is the google app password for that email address. Note the app password is not the same as your normal password and can be created by going to https://myaccount.google.com/apppasswords
```
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
qutoes=getQuotes()
products=getProducts()
invoices=getInvoices()
stockLevels=getStockLevels()

from skynamoInstanceDataClasses import My_Custom_Form_f23
formResults=getFormResults(My_Custom_Form_f23)
```
## Examples
Look in this repo's examples folder for some examples

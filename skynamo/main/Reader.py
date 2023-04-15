from .CreditRequest import CreditRequest
from .Order import Order
from .Quote import Quote
from .Product import Product
from .Customer import Customer

from skynamo.reader.jsonToObjects import getListOfObjectsFromJsonFile,populateCustomPropsFromFormResults,populateUserIdAndNameFromInteractionAndReturnFormIds
from skynamo.reader.sync import refreshJsonFilesLocallyIfOutdated,getSynchedDataTypeFileLocation
import json
from typing import List
from skynamo.reader.ReaderBase import ReaderBase
##|customImports|##

def _getTransactions(transactionClass,forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated([f'{transactionClass.__name__.lower()}s','completedforms','interactions'])#type:ignore
	interactionsJson={}
	with open(getSynchedDataTypeFileLocation('interactions'), "r") as read_file:
		interactionsJson=json.load(read_file)
	completedForms={}
	with open(getSynchedDataTypeFileLocation('completedforms'), "r") as read_file:
		completedForms=json.load(read_file)
	transactions=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation(f'{transactionClass.__name__.lower()}s'),transactionClass)
	populatedTransactions=[]
	for i,transaction in enumerate(transactions):
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(transaction,interactionsJson)
		try:
			populateCustomPropsFromFormResults(transaction,formIds,completedForms)
			populatedTransactions.append(transaction)
		except Exception as e:
			print(f'Warning: Error populating custom props for {transactionClass.__name__} {i}: {e}. Leaving out of transactions list since it might be because since the last sync new orders have come through but not yet their associated form results.')
	return populatedTransactions

class Reader(ReaderBase):
	def __init__(self):
		pass
	def getOrders(self,forceRefresh=False):
		orders:List[Order]=_getTransactions(Order,forceRefresh)
		return orders

	def getCreditRequests(self,forceRefresh=False):
		creditRequests:List[CreditRequest]=_getTransactions(CreditRequest,forceRefresh)
		return creditRequests

	def getQuotes(self,forceRefresh=False):
		quotes:List[Quote]=_getTransactions(Quote,forceRefresh)
		return quotes

	def getProducts(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['products'],forceRefresh)
		products:List[Product]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('products'),Product)
		return products

	def getCustomers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['customers'],forceRefresh)
		customers:List[Customer]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('customers'),Customer)
		return customers

	


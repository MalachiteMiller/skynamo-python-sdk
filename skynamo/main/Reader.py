from .CreditRequest import CreditRequest
from .Order import Order
from .Quote import Quote
from .Product import Product
from .Customer import Customer
from skynamo.models.Invoice import Invoice
from skynamo.models.User import User
from skynamo.models.Warehouse import Warehouse
from skynamo.models.Price import Price
from skynamo.models.StockLevel import StockLevel
from skynamo.reader.jsonToObjects import getListOfObjectsFromJsonFile,populateCustomPropsFromFormResults,populateUserIdAndNameFromInteractionAndReturnFormIds
from skynamo.reader.sync import refreshJsonFilesLocallyIfOutdated,getSynchedDataTypeFileLocation
import ujson
##|customImports|##

def _getTransactions(transactionClass,forceRefresh=False):
	refreshJsonFilesLocallyIfOutdated([f'{transactionClass.__name__.lower()}s','completedforms','interactions'])#type:ignore
	interactionsJson={}
	with open(getSynchedDataTypeFileLocation('interactions'), "r") as read_file:
		interactionsJson=ujson.load(read_file)
	refreshJsonFilesLocallyIfOutdated(['orders','completedforms','interactions'],forceRefresh)
	completedForms={}
	with open(getSynchedDataTypeFileLocation('completedforms'), "r") as read_file:
		completedForms=ujson.load(read_file)
	transactions=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation(f'{transactionClass.__name__.lower()}s'),transactionClass)
	for i,transaction in enumerate(transactions):
		formIds=populateUserIdAndNameFromInteractionAndReturnFormIds(transaction,interactionsJson)
		populateCustomPropsFromFormResults(transaction,formIds,completedForms)
	return transactions

class Reader:
	def __init__(self):
		pass
	def getOrders(self,forceRefresh=False):
		orders:list[Order]=_getTransactions(Order,forceRefresh)
		return orders

	def getCreditRequests(self,forceRefresh=False):
		creditRequests:list[CreditRequest]=_getTransactions(CreditRequest,forceRefresh)
		return creditRequests

	def getQuotes(self,forceRefresh=False):
		quotes:list[Quote]=_getTransactions(Quote,forceRefresh)
		return quotes

	def getProducts(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['products'],forceRefresh)
		products:list[Product]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('products'),Product)
		return products

	def getCustomers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['customers'],forceRefresh)
		customers:list[Customer]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('customers'),Customer)
		return customers

	def getInvoices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['invoices'],forceRefresh)
		invoices:list[Invoice]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('invoices'),Invoice)
		return invoices

	def getStockLevels(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['stocklevels'],forceRefresh)
		stockLevels:list[StockLevel]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('stocklevels'),StockLevel)
		return stockLevels

	def getUsers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['users'],forceRefresh)
		users:list[User]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('users'),User)
		return users

	def getWarehouses(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['warehouses'],forceRefresh)
		warehouses:list[Warehouse]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('warehouses'),Warehouse)
		return warehouses

	def getPrices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['prices'],forceRefresh)
		prices:list[Price]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('prices'),Price)
		return prices



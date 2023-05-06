from skynamo.models.Invoice import Invoice
from skynamo.models.User import User
from skynamo.models.Warehouse import Warehouse
from skynamo.models.TaxRate import TaxRate
from skynamo.models.Price import Price
from skynamo.models.StockLevel import StockLevel
from skynamo.models.PriceList import PriceList
from skynamo.models.VisitFrequency import VisitFrequency
from skynamo.reader.sync import refreshJsonFilesLocallyIfOutdated,getSynchedDataTypeFileLocation
from skynamo.reader.jsonToObjects import getListOfObjectsFromJsonFile,populateCustomPropsFromFormResults,populateUserIdAndNameFromInteractionAndReturnFormIds
from typing import List

class ReaderBase:
	def __init__(self):
		pass
	def getInvoices(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['invoices'], forceRefresh, key)
		invoices:List[Invoice]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('invoices'),Invoice)
		return invoices

	def getStockLevels(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['stocklevels'], forceRefresh, key)
		stockLevels:List[StockLevel]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('stocklevels'),StockLevel)
		return stockLevels

	def getUsers(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['users'], forceRefresh, key)
		users:List[User]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('users'),User)
		return users

	def getWarehouses(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['warehouses'], forceRefresh, key)
		warehouses:List[Warehouse]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('warehouses'),Warehouse)
		return warehouses

	def getPrices(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['prices'], forceRefresh, key)
		prices:List[Price]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('prices'),Price)
		return prices
	
	def getTaxRates(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['taxrates'], forceRefresh, key)
		taxRates:List[TaxRate]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('taxrates'),TaxRate)
		return taxRates
	
	def getPriceLists(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['pricelists'], forceRefresh, key)
		priceLists:List[PriceList]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('pricelists'),PriceList)
		return priceLists
	
	def getVisitFrequencies(self,forceRefresh=False, key: str = None):
		refreshJsonFilesLocallyIfOutdated(['visitfrequencies'], forceRefresh, key)
		visitFrequencies:List[VisitFrequency]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('visitfrequencies'),VisitFrequency)
		return visitFrequencies
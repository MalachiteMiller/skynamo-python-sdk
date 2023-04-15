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
	def getInvoices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['invoices'],forceRefresh)
		invoices:List[Invoice]=getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('invoices'),Invoice)
		return invoices

	def getStockLevels(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['stocklevels'],forceRefresh)
		stockLevels:List[StockLevel]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('stocklevels'),StockLevel)
		return stockLevels

	def getUsers(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['users'],forceRefresh)
		users:List[User]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('users'),User)
		return users

	def getWarehouses(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['warehouses'],forceRefresh)
		warehouses:List[Warehouse]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('warehouses'),Warehouse)
		return warehouses

	def getPrices(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['prices'],forceRefresh)
		prices:List[Price]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('prices'),Price)
		return prices
	
	def getTaxRates(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['taxrates'],forceRefresh)
		taxRates:List[TaxRate]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('taxrates'),TaxRate)
		return taxRates
	
	def getPriceLists(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['pricelists'],forceRefresh)
		priceLists:List[PriceList]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('pricelists'),PriceList)
		return priceLists
	
	def getVisitFrequencies(self,forceRefresh=False):
		refreshJsonFilesLocallyIfOutdated(['visitfrequencies'],forceRefresh)
		visitFrequencies:List[VisitFrequency]= getListOfObjectsFromJsonFile(getSynchedDataTypeFileLocation('visitfrequencies'),VisitFrequency)
		return visitFrequencies
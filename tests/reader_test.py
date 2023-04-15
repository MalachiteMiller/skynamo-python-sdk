import unittest
from skynamo import Reader
from skynamo import InstanceReader

class TestReader(unittest.TestCase):
	def test_GetAllCustomers(self):
		reader=Reader()
		customers=reader.getCustomers()
		self.assertNotEqual(len(customers),0)
		## find custom field test
		customField=customers[0].getCustomFieldWithName('Not exist I am sure of it')
		self.assertEqual(customField,None)
		customers[0].c999_Made_up_custom_field_='test'#type:ignore
		customField=customers[0].getCustomFieldWithName('Made up custom field ')
		self.assertEqual(customField,'test')

	def test_GetAllProducts(self):
		reader=Reader()
		products=reader.getProducts()
		self.assertNotEqual(len(products),0)
	def test_GetAllStockLevels(self):
		reader=InstanceReader()
		stockLevels=reader.getStockLevels()
		self.assertNotEqual(len(stockLevels),0)
	def test_GetAllUsers(self):
		reader=Reader()
		users=reader.getUsers()
		self.assertNotEqual(len(users),0)
	def test_GetAllInvoices(self):
		reader=Reader()
		invoices=reader.getInvoices()
		self.assertNotEqual(len(invoices),0)
	def test_GetAllQuotes(self):
		reader=Reader()
		quotes=reader.getQuotes()
		self.assertNotEqual(len(quotes),0)
	def test_GetAllCreditRequests(self):
		reader=Reader()
		creditRequests=reader.getCreditRequests()
		self.assertNotEqual(len(creditRequests),0)
	def test_GetAllOrders(self):
		reader=Reader()
		orders=reader.getOrders(forceRefresh=True)
		self.assertNotEqual(len(orders),0)
	def test_getWarehouses(self):
		reader=Reader()
		warehouses=reader.getWarehouses()
		self.assertNotEqual(len(warehouses),0)
	def test_getPrices(self):
		reader=Reader()
		prices=reader.getPrices()
		self.assertNotEqual(len(prices),0)
	def test_getCustomFormResults(self):
		reader=InstanceReader()
		##update according to instance being tested:
		customFormResults=reader.getAll_custom_field_types_f39()
		self.assertNotEqual(len(customFormResults),0)
		## find custom field test
		customField=customFormResults[0].getCustomFieldWithName('Not exist I am sure of it')
		self.assertEqual(customField,None)
		customFormResults[0].c999_Made_up_custom_field_='test'#type:ignore
		customField=customFormResults[0].getCustomFieldWithName('Made up custom field ')
		self.assertEqual(customField,'test')
	def test_getTaxRates(self):
		reader=Reader()
		taxRates=reader.getTaxRates()
		self.assertNotEqual(len(taxRates),0)
	def test_getVisitFrequencies(self):
		reader=Reader()
		visitFrequencies=reader.getVisitFrequencies(forceRefresh=True)
		self.assertNotEqual(len(visitFrequencies),0)
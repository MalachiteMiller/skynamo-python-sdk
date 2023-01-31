import unittest
from skynamo import updateInstanceDataClasses, getCreditRequests, getCustomers, getOrders, getProducts, getQuotes, getFormResults, getInvoices, getStockLevels

##test class that runs updateInstanceDataClasses before running all unittests
class TestGet(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		updateInstanceDataClasses()

	def test_getCreditRequests(self):
		creditRequests = getCreditRequests()
		#ensure each credit request has user id not 0 and user name not ""
		for creditRequest in creditRequests:
			self.assertTrue(creditRequest.user_id != 0)
			self.assertTrue(creditRequest.user_name != "")
		#ensure there are more than 0 credit requests
		self.assertTrue(len(creditRequests) > 0)

	def test_getOrders(self):
		orders = getOrders()
		#ensure each order has user id not 0 and user name not ""
		for order in orders:
			self.assertTrue(order.user_id != 0)
			self.assertTrue(order.user_name != "")
		#ensure there are more than 0 orders
		self.assertTrue(len(orders) > 0)

	def test_getQuotes(self):
		quotes = getQuotes()
		for quote in quotes:
			self.assertTrue(quote.user_id != 0)
			self.assertTrue(quote.user_name != "")
		##ensure there are more than 0 quotes
		self.assertTrue(len(quotes) > 0)

	def test_getCustomers(self):
		customers = getCustomers()
		self.assertTrue(len(customers) > 0)

	def test_getProducts(self):
		products = getProducts()
		self.assertTrue(len(products) > 0)


	def test_getInvoices(self):
		invoices = getInvoices()
		self.assertTrue(len(invoices) > 0)

	def test_getStockLevels(self):
		stockLevels = getStockLevels()
		self.assertTrue(len(stockLevels) > 0)

	def test_getFormResults(self):
		from skynamoInstanceDataClasses.All_custom_field_types_f39 import All_custom_field_types_f39
		formResults = getFormResults(All_custom_field_types_f39)
		self.assertTrue(len(formResults) > 0)
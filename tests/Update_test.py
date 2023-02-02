import unittest
from skynamo import updateInstanceDataClasses, getProducts,makeWrites,getCustomers
from skynamo.skynamoDataClasses.Address import Address

##test class that runs updateInstanceDataClasses before running all unittests
class TestUpdate(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		updateInstanceDataClasses()

	def test_updateProductNames(self):
		products = getProducts()
		writes=[]
		for product in products:
			if product.code in ['a','b','c']:
				product.name = "Test " + product.name
				writes.append(product.getWriteObjectToPatchProduct(["name"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)
		##assert that product names start with "Test "
		products = getProducts(forceRefresh=True)
		for product in products:
			if product.code in ['a','b','c']:
				self.assertTrue(product.name.startswith("Test "))
		##reset product names
		
		writes=[]
		for product in products:
			if product.code in ['a','b','c']:
				if product.name.startswith("Test "):
					product.name = product.code
					writes.append(product.getWriteObjectToPatchProduct(["name"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)

	def test_updateCustomerNames(self):
		customers=getCustomers()
		writes=[]
		for customer in customers:
			if customer.code in ['a','b','c']:
				customer.name = "Test " + customer.name
				writes.append(customer.getWriteObjectToPatchCustomer(["name"]))

		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)
		##assert that customer names start with "Test "
		customers = getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code in ['a','b','c']:
				self.assertTrue(customer.name.startswith("Test "))
		##reset customer names
		writes=[]
		for customer in customers:
			if customer.code in ['a','b','c']:
				if customer.name.startswith("Test "):
					customer.name = customer.code
					writes.append(customer.getWriteObjectToPatchCustomer(["name"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)

	def test_updateCustomFieldsInProducts(self):
		products = getProducts()
		writes=[]
		for product in products:
			if product.code in ['a','b','c']:
				product.c101_Categories="Option 1" #type:ignore
				writes.append(product.getWriteObjectToPatchProduct(["c101_Categories"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)
		##assert that all product categories updated correctly to Option 1
		products = getProducts(forceRefresh=True)
		for product in products:
			if product.code in ['a','b','c']:
				self.assertTrue(product.c101_Categories=="Option 1")
		#remove category from products
		writes=[]
		for product in products:
			if product.code in ['a','b','c']:
				if product.name.startswith("Test "):
					product.c101_Categories=None
					writes.append(product.getWriteObjectToPatchProduct(["name"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)

	def test_updateCustomFieldsInCustomers(self):
		customers=getCustomers()
		writes=[]
		for customer in customers:
			if customer.code in ['a','b','c']:
				customer.c4_Address=Address()
				customer.c4_Address.street="Test Street"
				customer.c4_Address.zip="Test Zip"
				writes.append(customer.getWriteObjectToPatchCustomer(["c4_Address"]))

		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)
		##assert that customer addresses were updated correctly
		customers = getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code in ['a','b','c']:
				if customer.c4_Address is not None:
					self.assertEqual(customer.c4_Address.street,"Test Street")
					self.assertEqual(customer.c4_Address.city,"")
					self.assertEqual(customer.c4_Address.zip,"Test Zip")
				else:
					self.fail("Customer address is None")
		#reset customer addresses
		writes=[]
		for customer in customers:
			if customer.code in ['a','b','c']:
				if customer.name.startswith("Test "):
					customer.c4_Address=None
					writes.append(customer.getWriteObjectToPatchCustomer(["name"]))
		errors=makeWrites(writes)
		self.assertTrue(len(errors)==0)

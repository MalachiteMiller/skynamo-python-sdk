import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
from skynamo import Address,Location
from datetime import datetime

reader=Reader()
writer=Writer()
testCustomersToUpdate=['a','b','c','d']

class TestCustomerUpdate(unittest.TestCase):
	def test_singleCustomerUpdateOfNonCustomFields(self):
		customers=reader.getCustomers()
		for customer in customers:
			if customer.code==testCustomersToUpdate[0]:
				customer.name='test_singleCustomerUpdateOfNonCustomField-after update'
				customer.price_list_id=2
				writer.addCustomerUpdate(customer,['name','price_list_id'])
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code==testCustomersToUpdate[0]:
				self.assertEqual(customer.name,'test_singleCustomerUpdateOfNonCustomField-after update')
				self.assertEqual(customer.price_list_id,2)
				customer.name='test_singleCustomerUpdateOfNonCustomField-before update'
				customer.price_list_id=1
				writer.addCustomerUpdate(customer,['name','price_list_id'])
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singleCustomerUpdateOfCustomFields(self):
		customers=reader.getCustomers()
		for customer in customers:
			if customer.code==testCustomersToUpdate[1]:
				customer.c4_Address=Address('test_singleCustomerUpdateOfCustomFields-after update',zip='test_singleCustomerUpdateOfCustomFields-after update',city='test_singleCustomerUpdateOfCustomFields-after update')
				writer.addCustomerUpdate(customer,['c4_Address'])
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code==testCustomersToUpdate[1]:
				if customer.c4_Address is None:
					self.fail('c4_Address should not be None')
				print(customer.c4_Address.getJsonReadyValue())
				self.assertEqual(customer.c4_Address.street,'test_singleCustomerUpdateOfCustomFields-after update')
				self.assertEqual(customer.c4_Address.zip,'test_singleCustomerUpdateOfCustomFields-after update')
				self.assertEqual(customer.c4_Address.city,'test_singleCustomerUpdateOfCustomFields-after update')
				customer.c4_Address=Address('test_singleCustomerUpdateOfCustomFields-before update',zip='test_singleCustomerUpdateOfCustomFields-before update',city='test_singleCustomerUpdateOfCustomFields-before update')
				writer.addCustomerUpdate(customer,['c4_Address'])
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_multipleCustomerUpdates(self):
		customers=reader.getCustomers()
		for customer in customers:
			if customer.code in testCustomersToUpdate:
				customer.name='test_multipleCustomerUpdates-after update'
				customer.price_list_id=2
				customer.c4_Address=Address('test_multipleCustomerUpdates-after update',zip='test_multipleCustomerUpdates-after update',city='test_multipleCustomerUpdates-after update')
				writer.addCustomerUpdate(customer,['name','price_list_id','c4_Address'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code in testCustomersToUpdate:
				if customer.c4_Address is None:
					self.fail('c4_Address should not be None')
				self.assertEqual(customer.name,'test_multipleCustomerUpdates-after update')
				self.assertEqual(customer.price_list_id,2)
				self.assertEqual(customer.c4_Address.street,'test_multipleCustomerUpdates-after update')
				self.assertEqual(customer.c4_Address.zip,'test_multipleCustomerUpdates-after update')
				self.assertEqual(customer.c4_Address.city,'test_multipleCustomerUpdates-after update')
				customer.name='test_multipleCustomerUpdates-before update'
				customer.price_list_id=1
				customer.c4_Address=Address('test_multipleCustomerUpdates-before update',zip='test_multipleCustomerUpdates-before update',city='test_multipleCustomerUpdates-before update')
				writer.addCustomerUpdate(customer,['name','price_list_id','c4_Address'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)


class TestCustomerReplace(unittest.TestCase):
	def test_singleCustomerReplaceOfNonCustomFields(self):
		customers=reader.getCustomers(forceRefresh=True)
		createDateBeforePut=datetime.now()
		locationBeforeUpdate=Location()
		for customer in customers:
			if customer.code==testCustomersToUpdate[3]:
				customer.name='test_singleCustomerReplaceOfNonCustomField-after update'
				customer.default_warehouse_id=None
				createDateBeforePut=customer.create_date
				locationBeforeUpdate=customer.location
				writer.addCustomerReplace(customer)
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code==testCustomersToUpdate[3]:
				self.assertEqual(customer.name,'test_singleCustomerReplaceOfNonCustomField-after update')
				self.assertEqual(customer.default_warehouse_id,None)
				self.assertEqual(customer.create_date,createDateBeforePut)
				self.assertEqual(customer.location.__dict__,locationBeforeUpdate.__dict__)
				customer.name='test_singleCustomerReplaceOfNonCustomField-before update'
				customer.default_warehouse_id=1
				writer.addCustomerReplace(customer)
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singleCustomerReplaceOfCustomFields(self):
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code==testCustomersToUpdate[0]:
				customer.c4_Address=None
				writer.addCustomerReplace(customer)
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		customers=reader.getCustomers(forceRefresh=True)
		for customer in customers:
			if customer.code==testCustomersToUpdate[0]:
				self.assertEqual(customer.c4_Address,None)
				customer.c4_Address=Address('test_singleCustomerReplaceOfCustomFields-before update',zip='test_singleCustomerReplaceOfCustomFields-before update',city='test_singleCustomerReplaceOfCustomFields-before update')
				writer.addCustomerReplace(customer)
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
		
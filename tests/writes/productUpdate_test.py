import unittest
from skynamo_data.code.Reader import Reader
from skynamo_data.code.Writer import Writer
from datetime import datetime
from skynamo import OrderUnit

reader=Reader()
writer=Writer()
testProductsToUpdate=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class TestProductUpdate(unittest.TestCase):
	def test_singleProductUpdateOfNonCustomFields(self):
		products=reader.getProducts()
		orderUnitsBeforeUpdate=[]
		for product in products:
			if product.code==testProductsToUpdate[0]:
				product.name='test_singleProductUpdateOfNonCustomField-after update'
				orderUnitsBeforeUpdate=product.order_units.copy()
				product.order_units=[OrderUnit('Unit after update',2)]
				writer.addProductUpdate(product,['name','order_units'])
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		products=reader.getProducts(forceRefresh=True)
		for product in products:
			if product.code==testProductsToUpdate[0]:
				self.assertEqual(product.name,'test_singleProductUpdateOfNonCustomField-after update')
				## check that first active order unit is 'Unit after update'
				for order_unit in product.order_units:
					if order_unit.active:
						self.assertEqual(order_unit.name,'Unit after update')
						self.assertEqual(order_unit.multiplier,2)
						break
				
				product.name='test_singleProductUpdateOfNonCustomField-before update'
				product.order_units=orderUnitsBeforeUpdate
				writer.addProductUpdate(product,['name','order_units'])
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleProductUpdateOfCustomFields(self):
		products=reader.getProducts()
		for product in products:
			if product.code==testProductsToUpdate[1]:
				product.name='test_singleProductUpdateOfCustomFields-after update'
				product.c101_Categories='Option 1'
				writer.addProductUpdate(product,['name','c101_Categories'])
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		products=reader.getProducts(forceRefresh=True)
		for product in products:
			if product.code==testProductsToUpdate[1]:
				self.assertEqual(product.name,'test_singleProductUpdateOfCustomFields-after update')
				self.assertEqual(product.c101_Categories,'Option 1')
				product.name='test_singleProductUpdateOfCustomFields-before update'
				product.c101_Categories='Option 2'
				writer.addProductUpdate(product,['name','c101_Categories'])
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_multipleProductUpdates(self):
		products=reader.getProducts()
		for product in products:
			if product.code in testProductsToUpdate:
				product.name='test_multipleProductUpdates-after update'
				writer.addProductUpdate(product,['name'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		products=reader.getProducts(forceRefresh=True)
		for product in products:
			if product.code in testProductsToUpdate:
				self.assertEqual(product.name,'test_multipleProductUpdates-after update')
				product.name='test_multipleProductUpdates-before update'
				writer.addProductUpdate(product,['name'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

class TestProductReplace(unittest.TestCase):
	def test_singleProductReplace(self):
		products=reader.getProducts()
		for product in products:
			if product.code==testProductsToUpdate[2]:
				product.name='test_singleProductReplace-after update'
				product.order_units=[OrderUnit('Unit after update',2)]
				writer.addProductReplace(product)
				break
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		products=reader.getProducts(forceRefresh=True)
		for product in products:
			if product.code==testProductsToUpdate[2]:
				self.assertEqual(product.name,'test_singleProductReplace-after update')
				## with a put operation order units are replaced, so there should be only one order unit
				self.assertEqual(product.order_units[0].name,'Unit after update')
				product.name='test_singleProductReplace-before update'
				product.order_units=[OrderUnit('Unit before update',1)]
				writer.addProductReplace(product)
				break
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_multipleProductReplaces(self):
		products=reader.getProducts()
		for product in products:
			if product.code in testProductsToUpdate:
				product.name='test_multipleProductReplaces-after update'
				writer.addProductReplace(product)
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		products=reader.getProducts(forceRefresh=True)
		for product in products:
			if product.code in testProductsToUpdate:
				self.assertEqual(product.name,'test_multipleProductReplaces-after update')
				product.name='test_multipleProductReplaces-before update'
				writer.addProductReplace(product)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

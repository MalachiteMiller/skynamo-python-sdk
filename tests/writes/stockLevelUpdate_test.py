import unittest
from skynamo_data.code.Writer import Writer

testProductsWithOrderUnits=[{'product_id':6,'code':'a','order_unit_id':9,'order_unit_name':'Unit'},{'product_id':7,'code':'b','order_unit_id':10,'order_unit_name':'Unit'}]

class TestStockLevelUpdate(unittest.TestCase):
	def test_singleStockLevelUpdateUsingProductAndOrderUnitIds(self):
		writer=Writer()
		writer.addStockLevelUpdate(testProductsWithOrderUnits[0]['product_id'],testProductsWithOrderUnits[0]['order_unit_id'],10)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singleStockLevelUpdateUsingProductCodeAndOrderUnitName(self):
		writer=Writer()
		writer.addStockLevelUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],testProductsWithOrderUnits[0]['order_unit_name'],12)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singleStockLevelUpdateUsingProductCodeAndOrderUnitNameAtSpecificWarehouse(self):
		writer=Writer()
		writer.addStockLevelUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],testProductsWithOrderUnits[0]['order_unit_name'],14,1)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_multipleStockLevelUpdatesUsingProductAndOrderUnitIds(self):
		writer=Writer()
		for product in testProductsWithOrderUnits:
			writer.addStockLevelUpdate(product['product_id'],product['order_unit_id'],16)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

class TestStockLevelUpdateErrors(unittest.TestCase):
	def test_singleStockLevelUpdateAtNonExistentProduct(self):
		writer=Writer()
		writer.addStockLevelUpdateUsingProductCodeAndUnitName('Idonot exist','Unit',16)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),1)
		self.assertEqual(writeErrors[0].dataType,'stocklevels')
		self.assertEqual(writeErrors[0].httpMethod,'post')
		self.assertEqual(writeErrors[0].error,["SL002: The product code 'Idonot exist' doesn't exist."])
	def test_singleStockLevelUpdateAtNonExistentOrderUnit(self):
		writer=Writer()
		writer.addStockLevelUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],'Idonot exist',16)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),1)
		self.assertEqual(writeErrors[0].dataType,'stocklevels')
		self.assertEqual(writeErrors[0].httpMethod,'post')
		self.assertEqual(writeErrors[0].error,["SL012: The supplied order unit name 'Idonot exist' doesn't correspond to current product.",
												"SL005: The order unit name 'Idonot exist' doesn't exist for this product."])

	def test_singleStockLevelUpdateAtNonExistentWarehouse(self):
		writer=Writer()
		writer.addStockLevelUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],testProductsWithOrderUnits[0]['order_unit_name'],16,999)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),1)
		self.assertEqual(writeErrors[0].dataType,'stocklevels')
		self.assertEqual(writeErrors[0].httpMethod,'post')
		self.assertEqual(writeErrors[0].error,["SL007: The warehouse id '999' doesn't exist."])
## follow similar strategy as in stockLevelUpdate_test.py
import unittest
from skynamo_data.code.Writer import Writer
from skynamo import OrderUnit

testProductsWithOrderUnits=[{'product_id':6,'code':'a','order_unit_id':9,'order_unit_name':'Unit'},{'product_id':7,'code':'b','order_unit_id':10,'order_unit_name':'Unit'}]
taxRateIdForTesting=9 #https://{testingInstance}.za.skynamo.me/TaxRates/Details/{taxRateIdForTesting}
priceListIdsForTesting=[1,2]

class TestPriceUpdate(unittest.TestCase):
	def test_singlePriceUpdateUsingProductAndOrderUnitIdsWithoutTaxRateId(self):
		writer=Writer()
		writer.addPriceUpdate(testProductsWithOrderUnits[0]['product_id'],testProductsWithOrderUnits[0]['order_unit_id'],10,priceListIdsForTesting[0])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singlePriceUpdateUsingProductAndOrderUnitIdsWithTaxRateId(self):
		writer=Writer()
		writer.addPriceUpdate(testProductsWithOrderUnits[0]['product_id'],testProductsWithOrderUnits[0]['order_unit_id'],11,priceListIdsForTesting[0],taxRateIdForTesting)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_singlePriceUpdateUsingProductCodeAndOrderUnitName(self):
		writer=Writer()
		writer.addPriceUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],testProductsWithOrderUnits[0]['order_unit_name'],12,priceListIdsForTesting[0])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_multiplePriceUpdatesUsingProductAndOrderUnitIds(self):
		writer=Writer()
		for product in testProductsWithOrderUnits:
			for priceListId in priceListIdsForTesting:
				writer.addPriceUpdate(product['product_id'],product['order_unit_id'],13,priceListId)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

class TestPriceUpdateErrors(unittest.TestCase):
	def test_singlePriceUpdateAtNonExistentPriceList(self):
		writer=Writer()
		writer.addPriceUpdateUsingProductCodeAndUnitName(testProductsWithOrderUnits[0]['code'],testProductsWithOrderUnits[0]['order_unit_name'],16,999)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),1)
		self.assertEqual(writeErrors[0].dataType,'prices')
		self.assertEqual(writeErrors[0].httpMethod,'post')
		self.assertEqual(writeErrors[0].error,["OUP007: The price list id '999' doesn't exist."])
	def test_singlePriceUpdateAtNonExistentProduct(self):
		writer=Writer()
		writer.addPriceUpdate(999,9,17,priceListIdsForTesting[0])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),1)
		self.assertEqual(writeErrors[0].dataType,'prices')
		self.assertEqual(writeErrors[0].httpMethod,'post')
		self.assertEqual(writeErrors[0].error,["OUP001: The product id '999' doesn't exist.","OUP013: The supplied product id '999' doesn't correspond to current order unit."])
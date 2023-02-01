import unittest
from skynamo import getStockLevelPutUsingProductCodeAndOrderUnitName,makeWrites


##todo add class method that ensure product used for tests exists in stead of hardcoding it based on what is in instance
class SingleStockLevelWritesUsingProductCodeAndOrderUnitName_test(unittest.TestCase):
	def test_useNullWarehouse(self):
		stockLevel = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 1)
		errors=makeWrites([stockLevel])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseId(self):
		stockLevel = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 2, warehouse_id=1)
		errors=makeWrites([stockLevel])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseName(self):
		stockLevel = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 3, warehouse_name="Location 123")
		errors=makeWrites([stockLevel])
		self.assertTrue(len(errors)==0)

class MultiStockLevelWritesUsingProductCodeAndOrderUnitName_test(unittest.TestCase):
	def test_useNullWarehouse(self):
		stockLevel1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 1)
		stockLevel2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 1)
		errors=makeWrites([stockLevel1,stockLevel2])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseId(self):
		stockLevel1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 2, warehouse_id=1)
		stockLevel2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 2, warehouse_id=1)
		errors=makeWrites([stockLevel1,stockLevel2])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseName(self):
		stockLevel1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 3, warehouse_name="Location 123")
		stockLevel2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 3, warehouse_name="Location 123")
		errors=makeWrites([stockLevel1,stockLevel2])
		self.assertTrue(len(errors)==0)

	def test_update26StockLevels(self):
		stockLevels=[]
		for i in range(26):
			alphabetLetter=chr(ord('a')+i)
			stockLevels.append(getStockLevelPutUsingProductCodeAndOrderUnitName(alphabetLetter, "Unit", i, warehouse_name="Location 123"))
		errors=makeWrites(stockLevels)
		self.assertTrue(len(errors)==0)
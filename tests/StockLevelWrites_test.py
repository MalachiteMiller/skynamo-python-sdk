import unittest
from skynamo import getStockLevelPutUsingProductCodeAndOrderUnitName,makeWrites
from skynamo import getStockLevels


##todo add class method that ensure product used for tests exists in stead of hardcoding it based on what is in instance
class SingleStockLevelWritesUsingProductCodeAndOrderUnitName_test(unittest.TestCase):
	def test_useNullWarehouse(self):
		stockLevelUpdate = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 1)
		errors=makeWrites([stockLevelUpdate])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseId(self):
		stockLevelUpdate = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 2, warehouse_id=1)
		errors=makeWrites([stockLevelUpdate])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseName(self):
		stockLevelUpdate = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 3, warehouse_name="Location 123")
		errors=makeWrites([stockLevelUpdate])
		self.assertTrue(len(errors)==0)

class MultiStockLevelWritesUsingProductCodeAndOrderUnitName_test(unittest.TestCase):
	def test_useNullWarehouse(self):
		stockLevelUpdate1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 1)
		stockLevelUpdate2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 1)
		errors=makeWrites([stockLevelUpdate1,stockLevelUpdate2])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseId(self):
		stockLevelUpdate1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 2, warehouse_id=1)
		stockLevelUpdate2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 2, warehouse_id=1)
		errors=makeWrites([stockLevelUpdate1,stockLevelUpdate2])
		self.assertTrue(len(errors)==0)

	def test_useWarehouseName(self):
		stockLevelUpdate1 = getStockLevelPutUsingProductCodeAndOrderUnitName("a", "Unit", 3, warehouse_name="Location 123")
		stockLevelUpdate2 = getStockLevelPutUsingProductCodeAndOrderUnitName("b", "Unit", 3, warehouse_name="Location 123")
		errors=makeWrites([stockLevelUpdate1,stockLevelUpdate2])
		self.assertTrue(len(errors)==0)

	def test_update26StockLevels(self):
		stockLevelUpdates=[]
		for i in range(26):
			alphabetLetter=chr(ord('a')+i)
			stockLevelUpdates.append(getStockLevelPutUsingProductCodeAndOrderUnitName(alphabetLetter, "Unit", i, warehouse_name="Location 123"))
		errors=makeWrites(stockLevelUpdates)
		self.assertTrue(len(errors)==0)
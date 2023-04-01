import unittest
from skynamo.integration_helpers import syncErpTaxRatesWithSkynamo, syncErpWarehousesWithSkynamo
from skynamo.main.Reader import Reader

class TestSyncTaxRatesAndWarehouses(unittest.TestCase):
	def test_syncErpTaxRatesWithSkynamo(self):
		syncErpTaxRatesWithSkynamo([{'id':'1','name':'15%', 'rate':'15', 'deleted_at':''},{'id':'2','name':'20%', 'rate':'20', 'deleted_at':''},{'id':'3','name':'25%', 'rate':'25', 'deleted_at':''}], 'id', 'name', 'rate')
		reader=Reader()
		taxRates=reader.getTaxRates(forceRefresh=True)
		expectedTaxRates={'15% (1)':15,'20% (2)':20,'25% (3)':25}
		##assert creation
		for taxR in taxRates:
			if taxR.name in expectedTaxRates:
				self.assertEqual(taxR.rate,expectedTaxRates[taxR.name])
				del expectedTaxRates[taxR.name]
		self.assertEqual(len(expectedTaxRates),0)
		## act update
		syncErpTaxRatesWithSkynamo([{'id':'1','name':'15%', 'rate':'15', 'deleted_at':''},{'id':'2','name':'18%', 'rate':'18', 'deleted_at':''},{'id':'3','name':'25%', 'rate':'25', 'deleted_at':'asdf'}], 'id', 'name', 'rate')
		nameThatShouldNotExist='20% (2)'
		taxRates=reader.getTaxRates(forceRefresh=True)
		expectedTaxRates={'15% (1)':15,'18% (2)':18,'25% (3)':25}
		##assert update
		for taxR in taxRates:
			if taxR.name in expectedTaxRates:
				self.assertEqual(taxR.rate,expectedTaxRates[taxR.name])
				if taxR.name=='25% (3)':
					self.assertEqual(taxR.active,False)
				else:
					self.assertEqual(taxR.active,True)
				del expectedTaxRates[taxR.name]
			if taxR.name==nameThatShouldNotExist:
				self.assertEqual(False,True)
		self.assertEqual(len(expectedTaxRates),0)
	def test_syncErpWarehousesWithSkynamo(self):
		syncErpWarehousesWithSkynamo([{'id':'1','name':'Warehouse 1', 'deleted_at':''},{'id':'2','name':'Warehouse 2', 'deleted_at':''},{'id':'3','name':'Warehouse 3', 'deleted_at':''}], 'id', 'name')
		reader=Reader()
		warehouses=reader.getWarehouses(forceRefresh=True)
		expectedWarehouses=['Warehouse 1 (1)','Warehouse 2 (2)','Warehouse 3 (3)']
		##assert creation
		for warehouse in warehouses:
			if warehouse.name in expectedWarehouses:
				del expectedWarehouses[expectedWarehouses.index(warehouse.name)]
		self.assertEqual(len(expectedWarehouses),0)
		## act update
		syncErpWarehousesWithSkynamo([{'id':'1','name':'Warehouse 1 v2', 'deleted_at':''},{'id':'2','name':'Warehouse 2', 'deleted_at':''},{'id':'3','name':'Warehouse 3', 'deleted_at':'asdf'}], 'id', 'name')
		nameThatShouldNotExist='Warehouse 1 (1)'
		warehouses=reader.getWarehouses(forceRefresh=True)
		expectedWarehouses=['Warehouse 1 v2 (1)','Warehouse 2 (2)','Warehouse 3 (3)']
		##assert update
		for warehouse in warehouses:
			if warehouse.name in expectedWarehouses:
				if warehouse.name=='Warehouse 3 (3)':
					self.assertEqual(warehouse.active,False)
				else:
					self.assertEqual(warehouse.active,True)
				del expectedWarehouses[expectedWarehouses.index(warehouse.name)]
			if warehouse.name==nameThatShouldNotExist:
				self.assertEqual(False,True)
		self.assertEqual(len(expectedWarehouses),0)

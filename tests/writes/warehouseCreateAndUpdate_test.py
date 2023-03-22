import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
import time

class TestWarehouseCreationAndUpdates(unittest.TestCase):
	def test_all(self):
		##arrange
		writer=Writer()
		warehouseName='TestWarehouse'+str(time.time())
		reader=Reader()
		##act create
		writer.addWarehouseCreate(warehouseName,"","","")
		writer.apply()
		##assert create
		warehouses=reader.getWarehouses(forceRefresh=True)
		warehouseNamesToWarehouses={w.name:w for w in warehouses}
		self.assertIn(warehouseName,warehouseNamesToWarehouses)
		##act update
		warehouseToUpdate=warehouseNamesToWarehouses[warehouseName]
		warehouseToUpdate.name=warehouseName+"Updated"
		writer.addWarehouseUpdate(warehouseToUpdate,['name'])
		writer.apply()
		##assert update
		warehouses=reader.getWarehouses(forceRefresh=True)
		warehouseNamesToIds={w.name:w.id for w in warehouses}
		self.assertIn(warehouseName+"Updated",warehouseNamesToIds)
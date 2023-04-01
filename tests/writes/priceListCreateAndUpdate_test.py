import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
import time

class WriterBaseTest(unittest.TestCase):
	def test_all(self):
		##arrange
		writer=Writer()
		priceListName='TestPriceList'+str(time.time())
		reader=Reader()
		##act create
		writer.addPriceListCreate(priceListName,True)
		errors=writer.apply()
		##assert create
		self.assertEqual(len(errors),0)
		priceLists=reader.getPriceLists(forceRefresh=True)
		priceListNamesToPriceLists={w.name:w for w in priceLists}
		self.assertIn(priceListName,priceListNamesToPriceLists)
		priceListToUpdate=priceListNamesToPriceLists[priceListName]
		self.assertEqual(priceListToUpdate.prices_include_vat,True)
		self.assertEqual(priceListToUpdate.active,True)
		##act update
		priceListToUpdate.name=priceListName+"Updated"
		priceListToUpdate.prices_include_vat=False
		priceListToUpdate.active=False
		writer.addPriceListUpdate(priceListToUpdate,['name','prices_include_vat','active'])
		errors=writer.apply()
		##assert update
		self.assertEqual(len(errors),0)
		priceLists=reader.getPriceLists(forceRefresh=True)
		priceListNamesToPriceLists={w.name:w for w in priceLists}
		self.assertIn(priceListName+"Updated",priceListNamesToPriceLists)
		priceListToUpdate=priceListNamesToPriceLists[priceListName+"Updated"]
		self.assertEqual(priceListToUpdate.prices_include_vat,False)
		self.assertEqual(priceListToUpdate.active,False)
		


import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
import time

class TestWriter(unittest.TestCase):
	def test_all(self):
		##arrange
		writer=Writer()
		reader=Reader()
		taxName='TestTax'+str(time.time())
		##act create
		writer.addTaxRateCreate(taxName,10.75,True)
		writer.apply()
		errors=writer.apply()
		##assert create
		self.assertEqual(len(errors),0)
		taxRates=reader.getTaxRates(forceRefresh=True)
		taxNamesToTaxRates={t.name:t for t in taxRates}
		self.assertIn(taxName,taxNamesToTaxRates)
		##act update
		taxToUpdate=taxNamesToTaxRates[taxName]
		taxToUpdate.name=taxName+"Updated"
		writer.addTaxRateUpdate(taxToUpdate,['name'])
		errors=writer.apply()
		##assert update
		self.assertEqual(len(errors),0)
		taxRates=reader.getTaxRates(forceRefresh=True)
		taxNamesToIds={t.name:t.id for t in taxRates}
		self.assertIn(taxName+"Updated",taxNamesToIds)
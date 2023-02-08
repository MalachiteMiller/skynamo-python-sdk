import unittest
from skynamo_data.code.Writer import Writer
from skynamo import OrderUnit
from datetime import datetime

class TestProductCreate(unittest.TestCase):
	def test_SingleProductCreateWithNoCustomFieldsAndSingleOrderUnit(self):
		writer=Writer()
		writer.addProductCreateWithSingleUnit(str(datetime.now()),'test_SingleProductCreateWithNoCustomFieldsAndSingleOrderUnit','Unit')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_SingleProductCreateWithNoCustomFieldsAndMultipleOrderUnits(self):
		writer=Writer()
		writer.addProductCreateWithMultipleOrderUnits(str(datetime.now()),'test_SingleProductCreateWithNoCustomFieldsAndMultipleOrderUnits',[OrderUnit('Unit1'),OrderUnit('Unit2'),OrderUnit('Unit3')])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def testSingleProductCreateWithCustomFieldsAndSingleOrderUnit(self):
		writer=Writer()
		writer.addProductCreateWithSingleUnit(str(datetime.now()),'testSingleProductCreateWithCustomFieldsAndSingleOrderUnit','Unit',c101_Categories='Option 2')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def testMultipleProductCreateWithCustomFieldsAndMultipleOrderUnits(self):
		writer=Writer()
		for i in range(10):
			writer.addProductCreateWithMultipleOrderUnits(str(datetime.now())+f'_{i}','testMultipleProductCreateWithCustomFieldsAndMultipleOrderUnits',[OrderUnit('Unit1'),OrderUnit('Unit2'),OrderUnit('Unit3')],c101_Categories='Option 2')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
## write a unit test class that tests the customerCreate function
import unittest
from skynamo_data.code.Writer import Writer
from datetime import datetime
from skynamo import Address

class TestCustomerCreate(unittest.TestCase):
	def test_singleCustomerCreateWithNoCustomFieldsNoPriceListAndNoWarehouse(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithNoCustomFieldsNoPriceListAndNoWarehouse')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithPriceListAndWarehouseIds(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithPriceListAndWarehouseIds',default_warehouse_id=1,price_list_id=2)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithPriceListName(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithPriceListName',price_list_name='Test')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithCustomAddressFieldFilledIn(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithCustomAddressFieldFilledIn',c4_Address=Address(street='test street',zip='12345'))
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithCustomTextFieldFilledIn(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithCustomTextFieldFilledIn',c108_Street_Address='test street')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithCustomNumberFieldFilledIn(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithCustomNumberFieldFilledIn',c6_Rank=2.2)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithCustomDateFieldFilledIn(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithCustomDateFieldFilledIn',c196_Custom_Date=datetime.now())
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_singleCustomerCreateWithCustomEnumField(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now()),'test_singleCustomerCreateWithCustomEnumField',c109_Default_Van='Option 1')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_multipleCustomerCreateWithPriceListWarehouseAndCustomFields(self):
		writer=Writer()
		writer.addCustomerCreate(str(datetime.now())+'_1','test_multipleCustomerCreateWithPriceListWarehouseAndCustomFields',default_warehouse_id=1,price_list_id=2,c4_Address=Address(street='test street',zip='12345'),c108_Street_Address='test street',c6_Rank=2.2,c196_Custom_Date=datetime.now(),c109_Default_Van='Option 1')
		writer.addCustomerCreate(str(datetime.now())+'_2','test_multipleCustomerCreateWithPriceListWarehouseAndCustomFields',default_warehouse_id=1,price_list_id=2,c4_Address=Address(street='test street',zip='12345'),c108_Street_Address='test street',c6_Rank=2.2,c196_Custom_Date=datetime.now(),c109_Default_Van='Option 1')
		writer.addCustomerCreate(str(datetime.now())+'_3','test_multipleCustomerCreateWithPriceListWarehouseAndCustomFields',default_warehouse_id=1,price_list_id=2,c4_Address=Address(street='test street',zip='12345'),c108_Street_Address='test street',c6_Rank=2.2,c196_Custom_Date=datetime.now(),c109_Default_Van='Option 1')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

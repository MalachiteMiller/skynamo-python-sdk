import unittest
from skynamo_data.code.Writer import Writer
from skynamo import InvoiceItem
from datetime import datetime

customerAtWhichToCreateTestInvoice='a'
productCodesToUseForTestInvoices=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

class TestInvoiceCreate(unittest.TestCase):
	def test_SingleInvoiceCreateWithOnlyRequiredFieldsAndSingleItem(self):
		writer=Writer()
		writer.addInvoiceCreate(datetime.now(),customerAtWhichToCreateTestInvoice,[InvoiceItem(productCodesToUseForTestInvoices[0],1,1.0)])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_SingleInvoiceCreateWithOnlyRequiredFieldsAndMultipleItems(self):
		writer=Writer()
		writer.addInvoiceCreate(datetime.now(),customerAtWhichToCreateTestInvoice,[InvoiceItem(productCodesToUseForTestInvoices[0],1,1.0),InvoiceItem(productCodesToUseForTestInvoices[1],2,2.0),InvoiceItem(productCodesToUseForTestInvoices[2],3,3.0)])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_SingleInvoiceCreateWithAllFieldsAndMultipleItems(self):
		writer=Writer()
		writer.addInvoiceCreate(datetime.now(),customerAtWhichToCreateTestInvoice,[InvoiceItem(productCodesToUseForTestInvoices[0],1,1.0),InvoiceItem(productCodesToUseForTestInvoices[1],2,2.0),InvoiceItem(productCodesToUseForTestInvoices[2],3,3.0,0.2)],'test_SingleInvoiceCreateWithAllFieldsAndMultipleItems','Paid',datetime(2023,1,1),False,5.5)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_MultipleInvoiceCreateWithAllFieldsAndMultipleItems(self):
		writer=Writer()
		for i in range(10):
			writer.addInvoiceCreate(datetime.now(),customerAtWhichToCreateTestInvoice,[InvoiceItem(productCodesToUseForTestInvoices[0],1,1.0),InvoiceItem(productCodesToUseForTestInvoices[1],2,2.0),InvoiceItem(productCodesToUseForTestInvoices[2],3,3.0,0.2)],f'test_SingleInvoiceCreateWithAllFieldsAndMultipleItems{i}','Paid',datetime(2023,1,1),False,5.5)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
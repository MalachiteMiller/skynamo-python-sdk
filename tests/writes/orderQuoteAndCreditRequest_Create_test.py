import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
from skynamo import LineItem
from datetime import datetime,timedelta

reader=Reader()
writer=Writer()

testCustomersAtWhichToCreateOrderQuoteAndCreditRequest=[6,7,8]
userIdAtWhichToCreateOrderQuoteAndCreditRequest=5
testProductCodesForOrders=['orderCreateTest1','orderCreateTest2','orderCreateTest3']

class TestCreateOrderQuoteAndCreditRequest(unittest.TestCase):
	## class method to ensure test products exist
	@classmethod
	def setUpClass(cls):
		try:
			for productCode in testProductCodesForOrders:
				writer.addProductCreateWithSingleUnit(productCode,productCode,'Unit')
			errors=writer.apply()
		except:
			pass
	def test_createOrderQuoteAndCreditRequestsWithoutTax(self):
		lineItems=[]
		for productCode in testProductCodesForOrders:
			lineItems.append(LineItem(productCode,1,'Unit',1,1.5,2.0))
		date=datetime.now()
		for customerCode in testCustomersAtWhichToCreateOrderQuoteAndCreditRequest:
			writer.addOrderCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
			writer.addQuoteCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
			writer.addCreditRequestCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
		writeErrors=writer.apply()
		self.assertEqual(writeErrors,[])

	def test_createOrderQuoteAndCreditRequestsWithTax(self):
		lineItems=[]
		for productCode in testProductCodesForOrders:
			lineItems.append(LineItem(productCode,1,'Unit',1,1.5,2.0,tax_rate_value=0.2))
		date=datetime.now()
		for customerCode in testCustomersAtWhichToCreateOrderQuoteAndCreditRequest:
			writer.addOrderCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
			writer.addQuoteCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
			writer.addCreditRequestCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems)
			date=date+timedelta(seconds=1)
		writeErrors=writer.apply()
		self.assertEqual(writeErrors,[])

	def test_createOrderQuoteAndCreditRequestWithCustomFields(self):
		lineItems=[]
		for productCode in testProductCodesForOrders:
			lineItems.append(LineItem(productCode,1,'Unit',1,1.5,2.0))
		date=datetime.now()
		for customerCode in testCustomersAtWhichToCreateOrderQuoteAndCreditRequest:
			writer.addOrderCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems,f5_c10_Comment='test_createOrderQuoteAndCreditRequestWithCustomFields')
			date=date+timedelta(seconds=1)
			writer.addQuoteCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems,f6_c14_Comment='test_createOrderQuoteAndCreditRequestWithCustomFields')
			date=date+timedelta(seconds=1)
			writer.addCreditRequestCreate(customerCode,date,userIdAtWhichToCreateOrderQuoteAndCreditRequest,lineItems,f7_c18_Comment='test_createOrderQuoteAndCreditRequestWithCustomFields')
			date=date+timedelta(seconds=1)
		writeErrors=writer.apply()
		self.assertEqual(writeErrors,[])
		orders=reader.getOrders(forceRefresh=True)
		self.assertEqual(orders[-1].f5_c10_Comment,'test_createOrderQuoteAndCreditRequestWithCustomFields')
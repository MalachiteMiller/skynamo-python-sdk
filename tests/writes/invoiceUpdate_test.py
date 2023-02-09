import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
from skynamo import InvoiceItem

reader=Reader()
writer=Writer()

testInvoiceIdsToUpdate=[5,6,7,8]

class TestInvoiceUpdate(unittest.TestCase):
	def test_updateReference(self):
		invoices=reader.getInvoices()
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				invoice.reference='test_updateReference-after update'
				writer.addInvoiceUpdate(invoice,['reference'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		invoices=reader.getInvoices(forceRefresh=True)
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				self.assertEqual(invoice.reference,'test_updateReference-after update')
				invoice.reference='test_updateReference-before update'
				writer.addInvoiceUpdate(invoice,['reference'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_updateCustomerCode(self):
		invoices=reader.getInvoices()
		customerCodesBeforeUpdate=[invoice.customer_code for invoice in invoices if invoice.id in testInvoiceIdsToUpdate]
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				invoice.customer_code='a'
				writer.addInvoiceUpdate(invoice,['customer_code'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		invoices=reader.getInvoices(forceRefresh=True)
		i=0
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				self.assertEqual(invoice.customer_code,'a')
				invoice.customer_code=customerCodesBeforeUpdate[i]
				i+=1
				writer.addInvoiceUpdate(invoice,['customer_code'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_updateItems(self):
		invoices=reader.getInvoices(forceRefresh=True)
		itemsBeforeUpdate=[invoice.items for invoice in invoices if invoice.id in testInvoiceIdsToUpdate]
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				invoice.items=[InvoiceItem('a',4,4),InvoiceItem('b',5,5),InvoiceItem('c',6,6)]
				writer.addInvoiceUpdate(invoice,['items'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		invoices=reader.getInvoices(forceRefresh=True)
		i=0
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				self.assertEqual(invoice.items[0].product_code,'a')
				self.assertEqual(invoice.items[0].quantity,4)
				self.assertEqual(invoice.items[0].totalLineValue,4)
				self.assertEqual(invoice.items[1].product_code,'b')
				self.assertEqual(invoice.items[1].quantity,5)
				self.assertEqual(invoice.items[1].totalLineValue,5)
				self.assertEqual(invoice.items[2].product_code,'c')
				self.assertEqual(invoice.items[2].quantity,6)
				self.assertEqual(invoice.items[2].totalLineValue,6)

				invoice.items=itemsBeforeUpdate[i]
				i+=1
				writer.addInvoiceUpdate(invoice,['items'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)

	def test_updateStatusAndBalanceDue(self):
		invoices=reader.getInvoices(forceRefresh=True)
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				invoice.status='Paid'
				invoice.outstanding_balance=0
				writer.addInvoiceUpdate(invoice,['status','outstanding_balance'])
		writeErrors=writer.apply()
		## assert and reset
		self.assertEqual(len(writeErrors),0)
		invoices=reader.getInvoices(forceRefresh=True)
		i=0
		for invoice in invoices:
			if invoice.id in testInvoiceIdsToUpdate:
				self.assertEqual(invoice.status,'Paid')
				self.assertEqual(invoice.outstanding_balance,0)

				invoice.status='Draft'
				invoice.outstanding_balance=5.0
				i+=1
				writer.addInvoiceUpdate(invoice,['status','outstanding_balance'])
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
import unittest
from skynamo import writeObjectToCsvWithObjectPropertiesAsColumnNames,sendEmailUsingGmailCredentialsWithFilesAttached

class OutputTest(unittest.TestCase):
	def test_writeObjectToCsv(self):
		class TestObject:
			def __init__(self):
				self.int = 1
				self.string = 'asdf'
				self.listOfStrings = ['asdf', 'qwer']
				self.listOfInts = [1, 2, 3]
				self.NoneType = None
				self.float = 1.111

		testObject = TestObject()
		writeObjectToCsvWithObjectPropertiesAsColumnNames(testObject, 'test.csv')
	
	def test_writeObjectToCsvWithSpecificColumnOrder(self):
		class TestObject:
			def __init__(self):
				self.int = 1
				self.string = 'asdf'
				self.listOfStrings = ['asdf', 'qwer']
				self.listOfInts = [1, 2, 3]
				self.NoneType = None
				self.float = 1.111

		testObject = TestObject()
		writeObjectToCsvWithObjectPropertiesAsColumnNames(testObject, 'testWithSpecificColOrder.csv', ['string', 'int', 'listOfStrings', 'listOfInts', 'NoneType', 'float'])

	def test_sendEmailUsingGmailCredentialsWithFilesAttached(self):
		sendEmailUsingGmailCredentialsWithFilesAttached('test', 'test', ['daniel@skynamo.com','servaas@skynamo.com'], ['test.csv'])
		
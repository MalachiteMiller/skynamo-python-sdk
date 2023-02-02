import unittest
from skynamo import writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames,sendEmailUsingGmailCredentialsWithFilesAttached

class OutputTest(unittest.TestCase):
	def test_writeListOfObjectsToCsv(self):
		class TestObject:
			def __init__(self,id:int):
				self.int = id
				self.string = 'asdf'
				self.listOfStrings = ['asdf', 'qwer']
				self.listOfInts = [1, 2, 3]
				self.NoneType = None
				self.float = 1.111

		testObject1 = TestObject(1)
		testObject2 = TestObject(2)
		writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames([testObject1,testObject2], 'test.csv')
	
	def test_writeListOfObjectsWithSpecificColumnOrder(self):
		class TestObject:
			def __init__(self,id:int):
				self.int = id
				self.string = 'asdf'
				self.listOfStrings = ['asdf', 'qwer']
				self.listOfInts = [1, 2, 3]
				self.NoneType = None
				self.float = 1.111

		testObject1 = TestObject(1)
		testObject2 = TestObject(2)
		writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames([testObject1,testObject2], 'testWithSpecificColumnOrder.csv', ['float','int'])

	def test_sendEmailUsingGmailCredentialsWithFilesAttached(self):
		sendEmailUsingGmailCredentialsWithFilesAttached('test', 'test', ['daniel@skynamo.com','servaas@skynamo.com'], ['test.csv'])
		
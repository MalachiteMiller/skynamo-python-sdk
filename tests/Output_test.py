import unittest
from skynamo import writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames,sendEmailUsingGmailCredentialsWithFilesAttached
import os

class TestCsvWriter(unittest.TestCase):
	def test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames(self):
		class TestObject:
			def __init__(self,a,b,c):
				self.a=a
				self.b=b
				self.c=c
		testObjects=[TestObject(1,2,3),TestObject(4,5,6),TestObject(7,8,9)]
		writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames(testObjects,'test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv')
		with open('skynamo_data/output/test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv','r') as f:
			lines=f.readlines()
		self.assertEqual(len(lines),4)
		self.assertEqual(lines[0].strip(),'"a","b","c"')
		self.assertEqual(lines[1].strip(),'"1","2","3"')
		self.assertEqual(lines[2].strip(),'"4","5","6"')
		self.assertEqual(lines[3].strip(),'"7","8","9"')
		os.remove('skynamo_data/output/test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv')

	def test_writeListOfObjectsToCsvWithSpecificColumnOrder(self):
		class TestObject:
			def __init__(self,a,b,c):
				self.a=a
				self.b=b
				self.c=c
		testObjects=[TestObject(1,2,3),TestObject(4,5,6),TestObject(7,8,9)]
		writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames(testObjects,'test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv',['b','c'])
		with open('skynamo_data/output/test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv','r') as f:
			lines=f.readlines()
		self.assertEqual(len(lines),4)
		self.assertEqual(lines[0].strip(),'"b","c","a"')
		self.assertEqual(lines[1].strip(),'"2","3","1"')
		self.assertEqual(lines[2].strip(),'"5","6","4"')
		self.assertEqual(lines[3].strip(),'"8","9","7"')
		os.remove('skynamo_data/output/test_writeListOfObjectsToCsvWithObjectPropertiesAsColumnNames.csv')

class TestEmailer(unittest.TestCase):
	def test_sendEmailUsingGmailCredentialsWithFilesAttached(self):
		fileName='test_sendEmailUsingGmailCredentialsWithFilesAttached.txt'
		with open(f'skynamo_data/output/{fileName}','w') as f:
				f.write('test')
		sendEmailUsingGmailCredentialsWithFilesAttached('test_sendEmailUsingGmailCredentialsWithFilesAttached','test_sendEmailUsingGmailCredentialsWithFilesAttached',['daniel@skynamo.com','jonathan@skynamo.com'],[fileName])
		os.remove(f'skynamo_data/output/{fileName}')
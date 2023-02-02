import os
from skynamo import updateInstanceDataClasses
import unittest

class TestUpdateInstanceDataClasses(unittest.TestCase):
	def test_UpdateInstanceDataClasses(self):
		## remove skynamoInstanceDataClasses folder with all subfolders and files
		if os.path.exists('skynamoInstanceDataClasses'):
			for root, dirs, files in os.walk('skynamoInstanceDataClasses', topdown=False):
				for name in files:
					os.remove(os.path.join(root, name))
				for name in dirs:
					os.rmdir(os.path.join(root, name))
			os.rmdir('skynamoInstanceDataClasses')
		## run updateInstanceDataClasses
		updateInstanceDataClasses()
		## check if skynamoInstanceDataClasses folder exists as well as Order.py, Quote.py, CreditRequest.py, Customer.py, Product.py, COVID_19_After_visit_checklist_f8.py
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses'))
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses/Order.py'))
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses/Quote.py'))
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses/CreditRequest.py'))
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses/Customer.py'))
		self.assertTrue(os.path.exists('skynamoInstanceDataClasses/Product.py'))
		#self.assertTrue(os.path.exists('skynamoInstanceDataClasses/COVID_19_After_visit_checklist_f8.py'))

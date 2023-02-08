from skynamo import refreshCustomFormsAndFields
import unittest

class TestRefreshCustomFormsAndFields(unittest.TestCase):
	def test_refreshCustomFormsAndFields(self):
		refreshCustomFormsAndFields()
		## review the generated code in skynamo_data/code if it matches the custom fields setup in this skynamo instance
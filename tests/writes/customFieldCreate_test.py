import unittest
from skynamo import CustomFieldsToCreate
from skynamo_data.code.Writer import Writer
customFormIdForTesting=39
class TestCustomFieldsToCreate(unittest.TestCase):
	def test_addSingleCustomerField(self):
		customFieldsToCreate=CustomFieldsToCreate()
		customFieldsToCreate.addCustomerCustomField('Test-Text','Text')
		writer=Writer()
		writer.addCustomFieldCreations(customFieldsToCreate)
		errors=writer.apply()
		self.assertEqual(len(errors),0)
	def test_addCustomerAndProductFieldsTogether(self):
		customFieldsToCreate=CustomFieldsToCreate()
		for fieldType in ['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address','UserSingleSelect','UserMultiSelect','HeadingLabel','NormalLabel','FinePrintLabel']:
			customFieldsToCreate.addCustomerCustomField('Test-'+fieldType,fieldType)#type:ignore
			customFieldsToCreate.addProductCustomField('Test-'+fieldType,fieldType)#type:ignore
		writer=Writer()
		writer.addCustomFieldCreations(customFieldsToCreate)
		errors=writer.apply()
		self.assertEqual(len(errors),0)
	def test_addCustomFormFields(self):
		customFieldsToCreate=CustomFieldsToCreate()
		for fieldType in ['Text','Number','SingleSelect','MultiSelect','NestedSingleSelect','NestedMultiSelect','Address','UserSingleSelect','UserMultiSelect','HeadingLabel','NormalLabel','FinePrintLabel']:
			customFieldsToCreate.addFormCustomField(customFormIdForTesting,'Test-'+fieldType,fieldType)#type:ignore
		writer=Writer()
		writer.addCustomFieldCreations(customFieldsToCreate)
		errors=writer.apply()
		self.assertEqual(len(errors),0)
	def test_addMultipleFieldsOfTheSameTypeToACustomForm(self):
		customFieldsToCreate=CustomFieldsToCreate()
		customFieldsToCreate.addFormCustomField(1,'Test-1','Text')
		customFieldsToCreate.addFormCustomField(1,'Test-2','Text')
		writer=Writer()
		writer.addCustomFieldCreations(customFieldsToCreate)
		errors=writer.apply()
		self.assertEqual(len(errors),0)

	def test_addMultipleFieldsOfTheSameTypeAndNameToACustomForm(self):
		customFieldsToCreate=CustomFieldsToCreate()
		customFieldsToCreate.addFormCustomField(1,'Test','Text')
		customFieldsToCreate.addFormCustomField(1,'Test','Text')
		writer=Writer()
		writer.addCustomFieldCreations(customFieldsToCreate)
		errors=writer.apply()
		self.assertEqual(len(errors),0)
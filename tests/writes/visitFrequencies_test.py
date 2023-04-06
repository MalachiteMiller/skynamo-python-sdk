import unittest
from skynamo_data.code.Writer import Writer
from skynamo_data.code.Reader import Reader
from typing import List,Literal

class TestWriter(unittest.TestCase):
	def setUp(self):
		self.writer=Writer()
		self.reader=Reader()
		self.testCustomerId=45 ## change this according to the instance you are testing on
		self.alternativeCustomerId=3 ## change this according to the instance you are testing on
		self.testUserName='Daniel' ## change this according to the instance you are testing on
		self.alternativeUserName='jean' ## change this according to the instance you are testing on
		try:
			self.writer.addVisitFrequencyCreate(self.testCustomerId,self.testUserName,1,1,'Week')
			errors=self.writer.apply()
		except:
			print('Visit frequency already exists')
			pass
	def test_periodChange(self):
		visitFreqs=self.reader.getVisitFrequencies()
		for visitFreq in visitFreqs:
			if visitFreq.customer_id==self.testCustomerId and visitFreq.user_name==self.testUserName:
				##update using different periods
				listOfOptions:List[Literal['Week','Month','Year']]=['Week','Month','Year','Month']
				for period in listOfOptions:
					visitFreq.period=period
					self.writer.addVisitFrequencyUpdate(visitFreq,['period'])
					errors=self.writer.apply()
					self.assertEqual(errors,[])

	def test_customerChange(self):
		visitFreqs=self.reader.getVisitFrequencies()
		for visitFreq in visitFreqs:
			if visitFreq.customer_id==self.testCustomerId and visitFreq.user_name==self.testUserName:
				visitFreq.customer_id=self.alternativeCustomerId
				self.writer.addVisitFrequencyUpdate(visitFreq,['customer_id'])
				errors=self.writer.apply()
				self.assertEqual(errors,[])

	def test_userChange(self):
		visitFreqs=self.reader.getVisitFrequencies()
		for visitFreq in visitFreqs:
			if visitFreq.customer_id==self.testCustomerId and visitFreq.user_name==self.testUserName:
				visitFreq.user_name=self.alternativeUserName
				self.writer.addVisitFrequencyUpdate(visitFreq,['user_name'])
				errors=self.writer.apply()
				self.assertEqual(errors,[])

	def test_cycleAndFrequencyChange(self):
		visitFreqs=self.reader.getVisitFrequencies()
		for visitFreq in visitFreqs:
			if visitFreq.customer_id==self.testCustomerId and visitFreq.user_name==self.testUserName:
				visitFreq.numberOfCyclesPerPeriod=2
				visitFreq.numberOfVisitsRequiredPerCycle=3
				self.writer.addVisitFrequencyUpdate(visitFreq,['numberOfCyclesPerPeriod','numberOfVisitsRequiredPerCycle'])
				errors=self.writer.apply()
				self.assertEqual(errors,[])
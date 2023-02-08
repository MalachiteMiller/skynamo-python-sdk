import unittest
from skynamo_data.code.Writer import Writer
userNameForTesting='Daniel'
customerForTesting='a'
from datetime import datetime

class TestScheduledVisitCreate(unittest.TestCase):
	def test_createScheduledVisitWithOnlyRequiredFields(self):
		writer=Writer()
		thisMonth=datetime.now().month
		thisYear=datetime.now().year
		nextMonth=thisMonth+1
		if nextMonth>12:
			nextMonth=1
			thisYear+=1
		dateTimeOneMonthLaterAccountingForYearChange=datetime(thisYear,nextMonth,1,8)
		writer.addScheduledVisitCreate(userNameForTesting,customerForTesting,dateTimeOneMonthLaterAccountingForYearChange)
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
	def test_createScheduledVisitWithAllFields(self):
		writer=Writer()
		thisMonth=datetime.now().month
		thisYear=datetime.now().year
		nextMonth=thisMonth+1
		if nextMonth>12:
			nextMonth=1
			thisYear+=1
		dateTimeOneMonthLaterAccountingForYearChange=datetime(thisYear,nextMonth,2,8)
		endTime=datetime(thisYear,nextMonth,2,23,0,0)
		writer.addScheduledVisitCreate(userNameForTesting,customerForTesting,dateTimeOneMonthLaterAccountingForYearChange,endTime,'Testing comment')
		writeErrors=writer.apply()
		self.assertEqual(len(writeErrors),0)
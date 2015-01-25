import sys
sys.path.append('../controllers/')
import pony.orm as pny
from transactions import TransactionsController
import unittest
import datetime
import pandas as pd
import matplotlib.pyplot as plt


class TestTransactionMethods(unittest.TestCase):
	
	#-----------------------------------------------------------------
	# query
	#-----------------------------------------------------------------
	
	def setUp(self):
		self.t = TransactionsController()
		self.today = datetime.datetime.today().strftime('%m/%d/%Y')
		self.first = datetime.datetime.today().strftime('%m/01/%Y')
	
	# def test_all_transactions(self):
	# 	self.t.get_transactions('fifth_third').to_data_frame()

	# def test_get_transactions(self):
	# 	date1 = '01/01/2015'
	# 	date2 = '01/08/2015'
	# 	num = 1
	# 	self.t.get_transactions('chase',date1,date2).to_data_frame()

	# def test_today(self):		
	# 	self.assertEqual(self.t.today(),self.today)

	# def test_first_of_month(self):
	# 	self.assertEqual(self.t.first_of_the_month(),self.first)
		
	# def test_days_ago(self):
	# 	self.t.days_ago(30)

	# def test_last_thirty(self):
	# 	ago = self.t.days_ago(30)
	# 	now = self.t.today()
	# 	self.t.get_transactions('fifth_third',ago,now).to_data_frame()
	
	# def test_this_month(self):
	# 	self.t.get_transactions('capitalone',self.first,self.today).to_data_frame()
	# def test_all_transactions(self):
	# 	self.t.get_transactions('fifth_third').to_data_frame()

	# def test_ft(self):
	# 	trans = self.t.get_transactions('fifth_third','12/01/2014','12/31/2014').to_data_frame()
	# 	print trans.groupby('Key').amount.sum()

	def test_chase(self):
		ft = self.t.get_transactions('fifth_third','12/01/2014','12/31/2014').to_data_frame()
		ch = self.t.get_transactions('chase','12/01/2014','12/31/2014').to_data_frame()
		list = ['PAYPAL','CHASE','CAPITAL','ELECTRONIC IMAGE','MUSICAL']

		trans = self.t.search_by_list(ft,list)

		
	#-----------------------------------------------------------------
	# utility
	#-----------------------------------------------------------------
	


	# def test_data_frame(self):
	# 	self.t.data_frame('fifth_third')

	# def test_account_count(self):
	# 	self.t.trans_count()

	# def test_find(self):
	# 	self.t.find('ELECTRONIC IMAGE')

	# def test_trans_exists(self):
	# 	self.t.trans_exists('ELECTRONIC IMAGE', 10)



	#-----------------------------------------------------------------
	# insert
	#-----------------------------------------------------------------
	
	# def test_insert(self):
	# 	self.t.insert('1/2/2015','Mortgage', 1400.00,1)

	
	#-----------------------------------------------------------------
	# delete
	#-----------------------------------------------------------------

	# def test_delete(self):
	# 	self.t.delete(2)


# this runs the tests
if __name__ == '__main__':
    unittest.main()


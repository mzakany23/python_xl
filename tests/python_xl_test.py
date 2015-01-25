import sys
sys.path.append('../lib/helper')
sys.path.append('../lib/controllers')
from python_xl import PythonXL, WorkBookInfo
from transactions import TransactionsController
import unittest


class TestPythonXL(unittest.TestCase):
	
	def setUp(self):
		path = '/Users/mzakany/Desktop/python_perfin/lib/csvs'
		file = '/Users/mzakany/Desktop/python_perfin/py_excel/perfin.xlsm'	
		self.x = PythonXL(path,file)
		self.t = TransactionsController()
		self.w = WorkBookInfo(file)
	 

	#-----------------------------------------------------
	# todo
	#-----------------------------------------------------
	
	# need to grab all files in csv folder 
	# and upload the most recent transactions to 
	# the database

	# then need to have functionality to grab
	# transactions from the database and add to excel

	#-----------------------------------------------------
	# csv folder
	#-----------------------------------------------------

	# 1. get all files 
	# 2. update the database with the recent transactions
	# 3. query and populate excel
	# 4. make chart

	#1
	# def test_show_csv_folder(self):
	# 	obj = self.x.show_csv_folder()
	# 	self.assertTrue(isinstance(obj,list))

	#2
	# def test_update_database(self):
	# 	self.x.update_database()

	#3
	# def test_update_xl_with_data_frames(self):
	# 	self.x.update_xl_with_data_frames('12/30/2014','01/05/2015')

	# run calculations

	# def test_calculations(self):
	# 	print self.x.get_calculations('fifth_third')

	# def test_run_all_calc(self):
	# 	print self.x.run_all_calculations()

	def test_to_xl(self):
		ft = self.t.get_transactions('fifth_third','12/01/2014','12/31/2014').to_data_frame()
		ch = self.t.get_transactions('chase','12/01/2014','12/31/2014').to_data_frame()
		list = ['PAYPAL','CHASE','CAPITAL','ELECTRONIC IMAGE','MUSICAL']
		trans = self.t.search_by_list(ft,list)
		print self.x.to_xl(trans)
		


	

if __name__ == '__main__':
    unittest.main()






















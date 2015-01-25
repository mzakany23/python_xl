import sys
sys.path.append('../lib/helper')
sys.path.append('../lib/controllers')
from python_xl import PythonXL, WorkBookInfo, Charts
from transactions import TransactionsController
from xlwings import Workbook, Range, Sheet
import pandas as pd
import matplotlib.pyplot as plt

import unittest

class TestAccountMethods(unittest.TestCase):
	def setUp(self):
		self.c = Charts()
		self.t = TransactionsController()
		self.file = '/Users/mzakany/Desktop/python_perfin/py_excel/perfin.xlsm'	


		


# this runs the tests
if __name__ == '__main__':
    unittest.main()

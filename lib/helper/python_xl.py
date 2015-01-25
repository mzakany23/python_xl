import os
import sys
sys.path.append('../controllers/')
# from transactions import TransactionsController
import glob
import numpy as np
import pandas as pd
from xlwings import Workbook, Range, Sheet

#-----------------------------------------------------
# charts
#-----------------------------------------------------
class Charts:
	def make_chart(self):
		pass
#-----------------------------------------------------
# workbook info class
#-----------------------------------------------------
class WorkBookInfo:

	def __init__(self,path):
		self.wb = Workbook(path)

	def sheets(self):
		self.wb
		names = map(lambda x: str(x.name) ,Sheet.all())
		for name in names:
			if name == 'fifth_third' or name == 'chase' or name == 'capitalone':
				continue
			else:
				names.remove(name)
		return names

#-----------------------------------------------------
# python_xl
#-----------------------------------------------------

class PythonXL(object):
	def __init__(self,path,file):
		self.path = path
		self.file = file
		self.files = self.__get_files_in_lib('csv','CSV')
		self.df_names = ['chase','fifth_third','captialone']

	
	def show_csv_folder(self):
		return self.files

	def update_database(self):
		paths = self.files
		for file in paths:
			name = self.__get_name(file)
			self.__upload_transactions(file,name)

	def update_xl_with_data_frames(self,d1=None,d2=None):
		s = WorkBookInfo(self.file)
		f = TransactionsController()
		if d1 == None and d2 == None:
			for name in s.sheets():
				Sheet(name).activate()
				Range('A1').value = f.get_transactions(name).to_data_frame()
		else:
			for name in s.sheets():
				Sheet(name).activate()
				Sheet(name).clear_contents()
				Range('A1').value = f.get_transactions(name,d1,d2).to_data_frame()

	def run_all_calculations(self):
		calc = {
			'fifth_third' : self.get_calculations('fifth_third'),
			'chase' : self.get_calculations('chase'),
			'capitalone' : self.get_calculations('capitalone')
		}

		Sheet('summary').activate()
		
		expenses = {
			'fifth_third' : 'B19',
			'chase' : 'B22',
			'captialone' : 'B25'
		}

		Range(expenses['fifth_third']).value = calc['fifth_third']['expenses_sum']
		Range(expenses['chase']).value = calc['chase']['expenses_sum']
		Range(expenses['captialone']).value = calc['capitalone']['expenses_sum']


	def get_calculations(self,name):
		Sheet(name).activate()
		data = Range('A1').table.value
		col = ['index','date','name','amount','payments','expenses','key']
		df = pd.DataFrame(data,columns=col).ix[1:]

		if name == 'capitalone':
			calc = {
				'payment_sum' :  df['payments'].sum(),
				'expenses_sum' : df['amount'].sum(),
				'key_count' : df.groupby('key').expenses.count(),
			}
		else: 
			calc = {
				'payment_sum' :  df['payments'].sum(),
				'expenses_sum' : df['expenses'].sum(),
				'key_count' : df.groupby('key').expenses.count(),
			}
		return calc
		
	def to_xl(self,trans):
		# WorkBookInfo(self.file)
		# Sheet('ft_list').activate()
		transactions = trans.get()
		# i = 1
		# x = 2
		# for key in transactions['found'].keys():
		# 	Range('A{i}'.format(**locals())).value = key
		# 	sum = 0
		# 	for line in transactions['found'][key]:
		# 		date = line[0]
		# 		name = line[1]
		# 		amount = line[2]
		# 		sum += amount
		# 		Range('B{x}'.format(**locals())).value = date
		# 		Range('C{x}'.format(**locals())).value = name
		# 		Range('D{x}'.format(**locals())).value = amount
		# 		x += 1
		# 	Range('E{x}'.format(**locals())).value = sum
		# 	x += 1
		# 	i = x

		for key in transactions['unfound']:
			print key

			
		



	# --------------------------------------------------
	# private
  # --------------------------------------------------

	def __upload_transactions(self,file,name):
  		t = TransactionsController()
	  	if name == 'venture':
	  	  t.upload_trans_from_file(file,'venture')
	  	elif name == 'united':
	  	  t.upload_trans_from_file(file,'united')
	  	elif name == '53':
	  	  t.upload_trans_from_file(file,'53')
	  	elif name == 'signature':
	  		t.upload_trans_from_file(file,'signature')

	
	def __get_files_in_lib(self,*types):
		path = self.path
		self.files = None
		t = []
		paths = []
		for x in types:
			t.append("/*%s" % x)
		for f in t:
			name = glob.glob(path+f)
			paths.extend(name)
		return map(str.lower,paths)
	
	def __get_names_in_lib(self):
		pass

	
	def __get_name(self,path):
		base = os.path.basename(path)
		return os.path.splitext(base)[0]

if __name__ == 'main':
	print 'main'






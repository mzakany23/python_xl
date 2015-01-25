import pony.orm as pny
import os
import sys
import glob
import numpy as np
import pandas as pd
import datetime
import re
from bs4 import BeautifulSoup
import subprocess
from xlwings import Workbook, Range, Sheet

#-----------------------------------------------------
# Utility Class
#-----------------------------------------------------

class Utility:
	def __init__(self):
		self.folder = os.listdir('/Users/mzakany/Desktop/python_perfin/lib/html/')

	def count(self,type):
		with pny.db_session:
			obj = pny.select(a for a in type).count()
			return obj

	def update_balances(self):
		""" runs the update balance script """
		""" supposed to scrape the balances from HTML and put on excel  """ 

		path = '/Users/mzakany/Desktop/python_perfin/lib/html/'
		f = self.__files_need_downloaded()
		if f is False:
			return 'nothing to do.'
		elif len(f) > 0:
			for file in self.folder:
				file_to_delete = os.path.join(path,file)
				os.unlink(file_to_delete)
			subprocess.Popen("pyperfin.sh")

	def scrape_html_folder(self):
		""" make dict of the balances """

		values = {
			'chase' : [],
			'fifth_third' : [],
			'capitalone' : []
		}
		for file in self.folder:
			
			account = self.__return_group(file).group('account')
			soup = BeautifulSoup(open(os.path.join('/Users/mzakany/Desktop/python_perfin/lib/html/',file)))
			if account == 'fifth_third':
				result = soup.find_all('td',class_='acctAvailable_Text')[0].text.replace('$','').replace(',','')
				values['fifth_third'].append(float(result))
			elif account == 'chase':
				result = soup.find_all('td',class_='summarylist')[1].text.replace('$','').replace(',','')
				values['chase'].append(float(result))
			elif account == 'capitalone':
				result = soup.find(id='ctlAccountsDashBoard_RptAccountsDashboard_ctl02_lblCurrentBalance').text.replace('$','').replace(',','')
				values['capitalone'].append(float(result))
		return values


	#----------------------------------------------------------------------------
	# private
	#----------------------------------------------------------------------------

	def __return_group(self,filename):
			match = '(?P<account>\w{0,11})_(?P<year>\d{4})_(?P<month>\d{2})_(?P<day>\d{2})_(?P<hour>\d{2})(?P<min>\d{2})'
			result = re.search(match,filename)
			return result

	def __files_need_downloaded(self):
			""" tells you what files need to be downloaded """
			""" if returns False then nothing needs downloaded """
			""" if ['fifth_third','chase'] then they both need downloaded """

			dates = []
			if self.folder.__len__() == 0:
				return False
			else:
				for name in self.folder:
					date = self.__return_group(name)
					account = str(date.group('account'))
					day = int(date.group('day'))
					month = int(date.group('month'))
					year = int(date.group('year'))
					today = datetime.date.today()
					formatted_date = datetime.date(year,month,day)
							
					if today > formatted_date:
						dates.append(account)
				
			return False if not dates else dates


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

class PythonXL:
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
			'fifth_third' : 'B24',
			'chase' : 'B27',
			'captialone' : 'B30'
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

#-----------------------------------------------------
# database and models
#-----------------------------------------------------

db = pny.Database('postgres', user='mzakany', password='zekezeke23', host='localhost', database='perfin', port=5555)

class Account(db.Entity):
	name = pny.Required(str)
	belongs_to = pny.Set("Transactions")

class Transactions(db.Entity):
	id = pny.PrimaryKey(int,auto=True)
	date = pny.Required(str)
	name = pny.Required(str)
	amount = pny.Required(float)
	account = pny.Required(Account)

db.generate_mapping(create_tables=True)

#-----------------------------------------------------
# database and models
#-----------------------------------------------------

class UtilityMethods:

	def count(self,type):
		with pny.db_session:
			obj = pny.select(a for a in type).count()
			return obj

#-----------------------------------------------------
# controllers
#-----------------------------------------------------

class TransactionsController(UtilityMethods):

	#-----------------------------------------------------------------
	# insert
	#-----------------------------------------------------------------

	@pny.db_session
	def upload_trans_from_file(self,path,name):
		if name == 'venture':
			self.__upload_csv(path,3)
		elif name == 'united':
			self.__upload_csv(path,2)
		elif name == '53':
			self.__upload_csv(path,1)
		elif name == 'signature':
			self.__upload_csv(path,3)


	#-----------------------------------------------------------------
	# query
	#-----------------------------------------------------------------

	@pny.db_session
	def find(self,match):
		q = pny.select(p for p in Transactions)	
		q2 = q.filter(name=match)
		return q2.show()

	
	@pny.db_session
	def get_transactions(self,name,d1=None,d2=None):
		if name == 'chase':
			account = Account.get(id=2)
		elif name == 'fifth_third':
			account = Account.get(id=1)
		elif name == 'capitalone':
			account = Account.get(id=3)

		self.arr = []
		if d1 == None and d2 == None:
			for x in account.belongs_to:
				self.arr.append([x.date,x.name,x.amount])
		else:
			beg_date = self.format_date(d1)
			end_date = self.format_date(d2)

			for tran in account.belongs_to:
				date = self.format_date(tran.date)
				if date > beg_date and date < end_date:
					self.arr.append([str(tran.date),str(tran.name),float(tran.amount)])
		return self

	@pny.db_session
	def all_transactions(self):
		trans_list = pny.select(t for t in Transactions)[:]
		self.arr = []
		for t in trans_list:
			self.arr.append([t.date,t.name,t.amount])
		return self

	

	#-----------------------------------------------------------------
	# utility
	#-----------------------------------------------------------------
	def to_data_frame(self):
		try:
			df = pd.DataFrame(self.arr,columns=['date','name','amount'])
			df['Payments'] = df['amount'].map(lambda x: x if x > 0 else 0)
			df['Expenses'] = df['amount'].map(lambda x: x if x < 0 else 0)
			df['Key'] = df['name'].map(lambda x: x[0:9].replace(' ',''))
			return df.sort(['date'],ascending=[0])
		except:
			pass

	def trans_count(self):
		return self.count(Transactions)

	@pny.db_session
	def trans_exists(self,dat,nam,amt):
		return pny.select(t for t in Transactions if t.name == nam and t.amount == amt and t.date == dat ).exists()

	def format_date(self,date):
		return datetime.datetime.strptime(str(date), '%m/%d/%Y')
	
	def days_ago(self,days_to_subtract):
		today = datetime.datetime.now()
		DD = datetime.timedelta(days=days_to_subtract)
		earlier = today - DD
		return earlier.strftime("%m/%d/%Y")

	def first_of_the_month(self):
		return datetime.datetime.now().strftime("%m/01/%Y")

	def today(self):
		today = datetime.datetime.today()
		return today.strftime('%m/%d/%Y')

	#-----------------------------------------------------------------
	# delete
	#-----------------------------------------------------------------

	@pny.db_session
	def delete(self,amt):
		trans = pny.select(t for t in Transactions).order_by(Transactions.name).limit(amt)
		for t in trans:
			t.delete()

	
	#-----------------------------------------------------
	#	private
	#-----------------------------------------------------

	@pny.db_session
	def __insert(self,date,name,amount,account):
		trans = Transactions(date=date,name=name,amount=amount,account=account)

	@pny.db_session
	def __upload_csv(self,path,account):

		df = pd.read_csv(path)

		for row in df.iterrows():
			if account == 1:
				date = row[1][0]
				name = row[1][1]
				amount = row[1][3]
			elif account == 2:
				date = row[1][2]
				name = row[1][3]
				amount = row[1][4]
			elif account == 3:
				date = row[1][0]
				name = row[1][2]
				amount = row[1][3]

			try:
				if self.trans_exists(date,name,amount):
					continue
				else:
					self.__insert(date,name,amount,account)
			except:
				continue		

class AccountController(UtilityMethods):
	
	def account_count(self):
		return self.count(Account)

	@pny.db_session
	def all(self):
		account_list = pny.select(a for a in Account)[:]
		return account_list

	@pny.db_session
	def insert(self,name):
		if pny.get(a for a in Account if a.name == name):
			return 'Name already exists'
		else:
			account = Account(id=id,name=name)









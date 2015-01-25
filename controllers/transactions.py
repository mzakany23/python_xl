import sys
sys.path.append('../models/')
sys.path.append('../lib/helper/')
import pony.orm as pny
import datetime
import time
from all_models import Transactions, Account
from utility_methods import UtilityMethods as u
from python_xl import PythonXL
import pandas as pd

class TransactionsController(u):
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

	def search_by_list(self,trans,list):
		found = {}
		unfound = {}
		self.transactions = {}
		data = trans.iterrows()

		for x in data:
			date = x[1][0]
			name = x[1][1]
			amount = x[1][2]

			word_found = False
			for word in list:
				if word in name:
					if found.has_key(word):
						found[word].append([date,name,amount])
					else:
						found[word] = []
						found[word].append([date,name,amount])
					word_found = True
			if not word_found:
				key = name[0:5].replace(' ','')
				line = [date,name,amount]
				if unfound.has_key(key):
					unfound[key].append(line)
				else:
					unfound[key] = []
					unfound[key].append(line)

		self.transactions['found'] = found
		self.transactions['unfound'] = unfound
		return self
	
	def get(self):
		return self.transactions

	def show(self):
		trans = self.transactions
		if trans['found'] is not None:
			print "Found Transactions:"
			for key in trans['found'].keys():
				sum = 0
				print key
				for line in trans['found'][key]:
					print line
					sum += line[2]
				print "{key} Total: {sum}".format(**locals())
		else:
			print 'there are no found transactions.'

		if trans['unfound'] is not None:
			print 'Unfound Transactions:'
			for key in trans['unfound'].keys():
				sum = 0
				print key
				for line in trans['unfound'][key]:
					sum += line[2]
					print line
				print "{key} Total: {sum}".format(**locals())
		else:
			print 'there are no unfound transactions.'
		
	def to_data_frame(self):
		try:
			df = pd.DataFrame(self.arr,columns=['date','name','amount'])
			df['Payments'] = df['amount'].map(lambda x: x if x > 0 else 0)
			df['Expenses'] = df['amount'].map(lambda x: x if x < 0 else 0)
			df['Key'] = df['name'].map(lambda x: x[0:9].replace(' ',''))
			return df.sort(['date'],ascending=[0])
		except:
			return 'There are no transactions in this range.'

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




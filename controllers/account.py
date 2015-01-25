import sys
sys.path.append('../models/')
sys.path.append('../lib/helper/')
import pony.orm as pny
from all_models import Account
from utility_methods import UtilityMethods as u

class AccountController(u):
	
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


import sys
sys.path.append('../controllers/')
import pony.orm as pny
from account import AccountController
import unittest


class TestAccountMethods(unittest.TestCase):
	
	#-----------------------------------------------------------------
	# query
	#-----------------------------------------------------------------
	
	def setUp(self):
		#this is like @variable in ruby
		self.a = AccountController()

	# should return total number accounts
	def test_account_count(self):
		self.assertEqual(self.a.account_count(), 4)

	# should return all accounts 
	# this is like Accounts.all in active record
	def test_all(self):
		self.assertEqual(len(self.a.all()),4)
	
	#-----------------------------------------------------------------
	# insert
	#-----------------------------------------------------------------
	
	def test_insert(self):
		self.assertEqual(self.a.insert('Chase2'),'Name already exists')
	


# this runs the tests
if __name__ == '__main__':
    unittest.main()
















# class Upload:
# 	def count(self,type):
# 		with pny.db_session:
# 			account = pny.select(a for a in type).count()
# 			return account

# u = Upload()

# print u.count(Account)
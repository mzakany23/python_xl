import pony.orm as pny

db = pny.Database('postgres', user='mzakany', password='zekezeke23', host='localhost', database='perfin')

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


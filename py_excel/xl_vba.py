import sys
sys.path.append('../lib/helper/')
from python_xl import PythonXL, TransactionsController, Utility
from xlwings import Workbook, Range, Sheet


# -----------------------------------------------------------------------------------------
# Excel vba callable functions
# -----------------------------------------------------------------------------------------
path = '/Users/mzakany/Desktop/python_perfin/lib/csvs'
file = '/Users/mzakany/Desktop/python_perfin/py_excel/perfin.xlsm'	
p = PythonXL(path,file)
t = TransactionsController()
u = Utility()
today = t.today()
first = t.first_of_the_month()
thirty_days_ago = t.days_ago(30)
sixty_days_ago = t.days_ago(60)

def update_xl_with_data_frames():
		wb = Workbook.caller()
		p.update_xl_with_data_frames()
		Sheet('summary').activate()

def this_months_transactions():
		wb = Workbook.caller()
		p.update_xl_with_data_frames(first,today)
		Sheet('summary').activate()		

def thirty_days():
		wb = Workbook.caller()
		p.update_xl_with_data_frames(thirty_days_ago,today)
		Sheet('summary').activate()	

def sixty_days():
		wb = Workbook.caller()
		p.update_xl_with_data_frames(sixty_days_ago,today)
		Sheet('summary').activate()	

def update_database():
		wb = Workbook.caller()
		p.update_database()

def run_calculations():
		wb = Workbook.caller()
		p.run_all_calculations()
		
def all_transactions_to_xl():
		wb = Workbook.caller()
		Sheet('all_transactions').activate()
		Range('A1').value = t.all_transactions().to_data_frame()
		Sheet('summary').activate()

def refresh_balances():
		wb = Workbook.caller()
		Sheet('summary').activate()
		u = Utility()
		values = u.scrape_html_folder()
		Range('B13').value = values['fifth_third'][0]
		Range('C13').value = values['chase'][0]
		Range('E13').value = values['capitalone'][0]
		


if __name__ == 'main':
	update_xl_with_data_frames()

	


from utility_methods import UtilityMethods
from xlwings import Workbook, Range, Sheet

def refresh_balances_xl():
		wb = Workbook('../../py_excel/perfin.xlsm')
		Sheet('summary').activate()
		u = UtilityMethods()
		values = u.scrape_html_folder()
		Range('B13').value = values['fifth_third'][0]
		Range('C13').value = values['chase'][0]
		Range('E13').value = values['capitalone'][0]

refresh_balances_xl()
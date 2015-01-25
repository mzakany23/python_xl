import pony.orm as pny
import os
import re
import datetime
import subprocess
from bs4 import BeautifulSoup

class UtilityMethods:
	def __init__(self):
		self.folder = os.listdir('../html/')

	def count(self,type):
		with pny.db_session:
			obj = pny.select(a for a in type).count()
			return obj

	def update_balances(self):
		""" runs the update balance script """
		""" supposed to scrape the balances from HTML and put on excel  """ 

		path = '/Users/mzakany/Desktop/python_perfin/lib/html/'
		f = self.__files_need_downloaded()
		if len(f) > 0:
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
			soup = BeautifulSoup(open(os.path.join('../html/',file)))
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





			





	
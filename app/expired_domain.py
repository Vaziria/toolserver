from urllib.parse import urlencode
import os
import pickle
import traceback

from lxml import etree
from io import StringIO, BytesIO
from requests import Session

from vazutils.http import CommonRequest
from vazutils.logger import Logger

logger = Logger(__name__)

class TableNotFound(Exception):
	pass

class ExpiredDomain(CommonRequest):

	username = None
	password = None
	session = None

	def __init__(self, user, pwd):
		self.username = user
		self.password = pwd


	def init_session(self):
		fname = 'data/session/{}.cache'.format(self.username)
		if os.path.exists(fname):
			with open(fname, 'r+b') as out:
				self.__dict__.update(pickle.load(out))

			logger.info("[ {} ] using session lama".format(self.username))
			return True

		else:

			logger.info("[ {} ] session Baru".format(self.username))
			self.session = Session()

			return self.login()

	def save_session(self):

		fname = 'data/session/{}.cache'.format(self.username)
		with open(fname, 'w+b') as out:
			pickle.dump(self.__dict__, out)


	def member_url(self, path, query = {}):

		query = urlencode(query)

		if query == '':
			url = 'https://member.expireddomains.net/{}'.format(path)
		else:
			url = 'https://member.expireddomains.net/{}?{}'.format(path, query)

		return url




	def login(self):
		url = "https://member.expireddomains.net/login/"

		headers = {
			'Accept': 'ext/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'Content-Type': 'application/x-www-form-urlencoded',
			'Origin': 'null',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36'
		}

		payload = {
			'login': self.username,
			'password': self.password,
			'redirect_to_url': '/beginpage',
			'rememberme': 1
		}

		req = self.CRequest('post', url, headers = headers, data = urlencode(payload))

		if req.url == "https://member.expireddomains.net/":
			logger.info('[ {} ] logged'.format(self.username))
			return True

		os.remove('data/session/{}.cache'.format(self.username))
		logger.error('[ {} ] gagal login'.format(self.username))

		return False


	def get_expired(self, start = 0, post = False):

		urlparam = {
				'start': start,
				'fonlycharhost': 1
			}

		url = self.member_url('domains/combinedexpired/', urlparam)

		headers = {
			# 'Referer': 'https://member.expireddomains.net/',
			'Origin': 'expireddomains.net',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
		}

		if post:
			url = self.member_url('domains/combinedexpired/')

			req = self.CRequest('post', url, headers = headers, data=urlencode({'fonlycharhost': 1}))
		else:
			req = self.CRequest('get', url, headers = headers)

		# self.test(req.text)



		parser = etree.HTMLParser()
		tree = etree.parse(StringIO(req.text), parser)

		try:
			table = tree.xpath('//*/table[@class="base1"]')[0]
		except IndexError as e:
			raise TableNotFound
			
		try:
			count = tree.xpath('//*/div[@class="infos form-inline"]/strong/text()')[1]
		except IndexError as e:
			raise TableNotFound

		count = int(count.replace(',', ''))

		return [count, self.parse_table(table)]


	def parse_table(self, table):



		# keys = table.xpath('thead/tr/th/a/text()')
		# keys = list(map(lambda x: x.lower(), keys))

		for row in table.xpath('tbody/tr'):
			try:
				tds = row.xpath('td')
				domain = tds[0].xpath('a/text()')[0]
				available = tds[22].xpath('a/text()')[0]

				if available == "available":
					yield domain

			except Exception as e:
				traceback.print_exc()



		


	def test(self, text):

		with open('test.html', 'w+', encoding="utf8") as out:
			out.write(text)



if __name__ == '__main__':

	test = ExpiredDomain('bimaseptian7', 'Balikpapan1*')

	if test.init_session():
		print('get domain')

		count, domain = test.get_expired()

		for item in domain:
			print(item)

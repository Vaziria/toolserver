from urllib.parse import urlencode
import os
import pickle
import traceback
import copy

from lxml import etree
from io import StringIO, BytesIO
from requests import Session

from . import var_domain 

from vazutils.http import CommonRequest
from vazutils.logger import Logger

logger = Logger(__name__)

class TableNotFound(Exception):
	pass

class ExpiredDomain(CommonRequest):

	username = None
	password = None
	session = Session()
	path_domain = None
	query = {}

	def __init__(self, user, pwd, path_domain = 'domains/expiredcom/', query = {}):
		self.username = user
		self.password = pwd
		self.path_domain = path_domain
		self.query = query

		logger.info('using query {}'.format(self.query))


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
			'redirect_to_url': '/startpage',
			'rememberme': 1
		}

		req = self.CRequest('post', url, headers = headers, data = urlencode(payload))

		if req.url == "https://member.expireddomains.net/":
			logger.info('[ {} ] logged'.format(self.username))
			return True

		os.remove('data/session/{}.cache'.format(self.username))

		with open('gagal.html', 'w+', encoding = 'utf8') as out:
			out.write(req.text)
		
		logger.error('[ {} ] gagal login'.format(self.username))

		return False


	def get_expired(self, start = 0):

		headers = {
			'Referer': 'https://member.expireddomains.net/{}'.format(self.path_domain),
			'Origin': 'expireddomains.net',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36',
		}

		if start == 0:

			payload = copy.deepcopy(var_domain.payload)
			payload.update(self.query)

			payload_post = urlencode(payload)
			url = self.member_url('domains/expiredcom/#listing')

			req = self.CRequest('post', url, headers = headers, data=payload_post, timeout=30)

		else:

			headers['Referer'] = 'https://member.expireddomains.net/{}?start=100&flimit=100&fonlycharhost=1#listing'.format(self.path_domain)

			urlparam = {
					'start': start,
					'fonlycharhost': 1
				}

			urlparam.update(self.query)

			url = self.member_url(self.path_domain, urlparam) + '#listing'

			req = self.CRequest('get', url, headers = headers, timeout=30)


		# if post:
		# 	url = self.member_url('domains/combinedexpired/')
		# else:
		# 	req = self.CRequest('get', url, headers = headers, timeout=30)

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

	test = ExpiredDomain('pardok', 'heri7777')

	if test.login():
		print('get domain')

		count, domain = test.get_expired()

		for item in domain:
			print(item)

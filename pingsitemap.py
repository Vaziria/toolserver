from gevent import monkey
	
monkey.patch_all()

from gevent.pool import Pool
import requests

from vazutils.logger import Logger
from vazutils.useragent import _useragent
from vazutils.file_format import FileFormat

logger = Logger(__name__) 


class PingSitemap:

	thread_count = 10
	path_sitemap = '/sitemap.xml'

	def __init__(self, filename):
		self.file = FileFormat(filename, [], [ 'domain' ])


	def ping(self, url):

		url = "https://www.google.com/webmasters/tools/ping?sitemap={}".format(url)

		headers = {
			'User-Agent': _useragent.get(),
			'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
			'accept-encoding': 'gzip, deflate, br',
			'accept-language': 'en-US,en;q=0.9',
			'cache-control': 'no-cache',
			'pragma': 'no-cache',
			'sec-fetch-dest': 'document',
			'sec-fetch-mode': 'navigate',
			'sec-fetch-site': 'none',
		}

		# print(headers)
		# print(url)

		req = requests.get(url, headers = headers)

		return req.status_code == 200




	def run(self):
		for domain in self.file.data:
			url = 'https://{}{}'.format(domain['domain'], self.path_sitemap)

			if self.ping(url):
				logger.info('sitemap {} submitted'.format(domain['domain']))




if __name__ == '__main__':
	import argparse

	parser = argparse.ArgumentParser(description='Ping sitemap')
	parser.add_argument('file', type=str, help='file subdomain')

	args = parser.parse_args()

	runner = PingSitemap(args.file)
	runner.run()




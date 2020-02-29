import time
import random


from app.expired_domain import ExpiredDomain, TableNotFound
from vazutils.logger import Logger

logger = Logger(__name__)



class GetDomain:

	thread_count = 10
	user = ExpiredDomain('bimaseptian7', 'Balikpapan1*')
	pref_name = 'domainexpired/domain_{}.txt'
	delay = [0, 5]


	def __init__(self):
		self.user.init_session()


	def saver(self):
		while self.saver_run and self.domains.__len__() == 0:

			try:
				domain = self.domains.pop(0)
				self.write(domain+'\n')
			except IndexError as e:
				pass

			time.sleep(0.01)


	def get_task(self):

		count, hasil = self.user.get_expired()

		for domain in hasil:
			self.domains.append(domain)

		c = 25
		while c < count:

			yield {
				'func': self.get_page,
				'option': c
			}

			c = c + 25


	def get_page(self, start):

		count, hasil = self.user.get_expired(start)

		for domain in hasil:
			self.domains.append(domain)



	def write(self, domain):

		with open('domain.txt', 'a+') as out:
			out.write(domain)

		logger.info('save {}'.format(domain))




	def run(self):
		try:
			count, hasil = self.user.get_expired()
		except TableNotFound:
			count, hasil = self.user.get_expired(post=True)

		for domain in hasil:
			self.write(domain)

		c = 25
		while c < count:
			secs = random.randint(*self.delay)
			time.sleep(secs)
			logger.info('sleep {} second'.format(secs))

			try:
				count, hasil = self.user.get_expired(c)
			except TableNotFound:
				logger.info(c)
				time.sleep(secs)
				logger.info('sleep {} second'.format(20))
				count, hasil = self.user.get_expired(post=True)
				continue

			for domain in hasil:
				self.write(domain)

			c = c + 25





if __name__ == '__main__':

	tasker = GetDomain()

	tasker.run()





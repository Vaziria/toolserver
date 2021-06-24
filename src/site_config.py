import requests
import random
import json

class SiteConfig:
    domain: str = ''
    pwd: str = ''
    protocol = 'http://'
    dataurl = {}

    def __init__(self, domain, pwd, http = False):
        self.domain = domain
        self.pwd = pwd
        if http:
            self.protocol = 'http://'
        else:
            self.protocol = 'https://'

        with open('url.json', 'r') as out:
            self.dataurl = json.load(out)
            url = '{}{}'.format(self.protocol, self.domain)
    
    def random_config(self, sub = False):
        config = {
            "url_single": random.choice(self.dataurl['url_single']),
            "url_category": random.choice(self.dataurl['url_category']),
            "url_sitemap": random.choice(self.dataurl['url_sitemap']),
            "url_image": random.choice(self.dataurl['url_image']),
            "tema": random.choice(self.dataurl['tema']),
            "lang": random.choice(self.dataurl['lang']),
        }

        if random.choice([True, False]):
            config['url_encript'] = 'on'

        if random.choice([True, False]):
            config['local_image'] = 'on'

        self.configure(config, sub)

    def configure(self, data, sub = False):

        config = {
            'site_title':  '[server_name] --> [custom_category] | {best Seller|Deal Sale} Online Shopping',
            'site_desc': 'bambank desc testasdasd',
            'limit_page': '20',
            # 'url_encript': 'on',
            # 'debug': 'on',
            'base_url': '',
            # 'lang': 'en',
            # 'tema': 'breivik',
            # 'url_single': '/product/{id}/{title}.html',
            # 'url_category': '/categoury-{id}/{key}.html',
            # 'url_sitemap': '/{level}-{page}-product-{key}.xml',
            # 'local_image': 'on',
            # 'url_image': '/image/{id}/{name}.jpg',
            'save': ''
        }

        config.update(data)

        if sub:
            url = '{}{}.{}/admin?pass={}'.format(self.protocol, sub, self.domain, self.pwd)
        else:
            url = '{}{}/admin?pass={}'.format(self.protocol, self.domain, self.pwd)

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36"
        }

        print(url)
        req = requests.post(url, data = config)

if __name__ == '__main__':

    config = SiteConfig('glenbrookmall.club', 'sodosaler')
    config.random_config('women-clothing-accessories')

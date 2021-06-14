import json
from src.file_ns import FileNs
from src.site_config import SiteConfig

class RandomizerConfig:
    domain: str = ''
    ip: str = ''
    subdomain = []
    ns: FileNs = None

    def __init__(self, name, ip):
        self.domain = name
        self.ip = ip
        self.ns = FileNs(name, ip)
    
    def get_categ(self):
        fname = 'alicateg'

        with open (fname, 'r') as out:
            datas = json.load(out)

        for data in datas:
            if data['level'] > 2:
                continue

            yield data


    def run(self):
        
        for categ in self.get_categ():
            key = categ['key']

            self.ns.add(key)
            print('create {}.{}'.format(key, self.domain))
            # config = SiteConfig(self.domain, 'sodosaler')
            # config.random_config(key)

        self.ns.save()

    def randomConfig(self):
        for sub in self.ns.get_sub():
            config = SiteConfig(self.domain, 'sodosaler')
            print('configuring {}'.format(sub['sub']))
            config.random_config(sub['sub'])


if __name__ == '__main__':
    domain = RandomizerConfig('glenbrookmall.club', '45.77.173.71')

    # domain.run()
    domain.randomConfig()
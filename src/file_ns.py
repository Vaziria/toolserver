from typing import NamedTuple, List
import json
import os
import sys

_isi = """
;; A Records
{domain}.	1	IN	A	{ip}
"""

_line = "{sub}.{domain}.	1	IN	A	{ip}\n"


class SubItem(NamedTuple):
    sub: str
    domain: str
    ip: str

class FileNs:
    data: List[SubItem] = []
    domain: str = ''
    ip: str = ''

    def __init__(self, domain, ip):
        self.data = []
        self.domain = domain
        self.ip = ip
    
    def get_sub(self):
        fname = 'datadomain/{}/{}_sublist.txt'.format(self.domain, self.domain)
        with open(fname, 'r') as out:
            return json.load(out)

    def add(self, key):
        data = {
            'sub': key,
            'domain': self.domain,
            'ip': self.ip
        }

        self.data.append(data)

    def save(self):
        
        if not os.path.exists('datadomain/{}'.format(self.domain)):
            os.makedirs('datadomain/{}'.format(self.domain))
        
        first = True

        fname = 'datadomain/{}/{}.txt'.format(self.domain, self.domain)

        with  open(fname, 'w+') as out:
            for data in self.data:
                # if first:
                #     payload = _isi.format(**data)
                #     first = False
                # else:
                payload = _line.format(**data)

            
                out.write(payload)

        fname = 'datadomain/{}/{}_sublist.txt'.format(self.domain, self.domain)
        with  open(fname, 'w+') as out:
            json.dump(self.data, out)
import argparse
import random



_isi = """
;; A Records
{domain}.	1	IN	A	{ip}
"""



parser = argparse.ArgumentParser(description='Random NameServer')
parser.add_argument('file', type=str, help='file')

args = parser.parse_args()
print(args.accumulate(args.integers))
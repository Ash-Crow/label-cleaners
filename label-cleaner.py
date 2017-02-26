# from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import requests

# Constants 
base_url = 'https://www.wikidata.org'
api_url = base_url + '/w/api.php'


def getWDinfo(qids):
        payload = {
            'action': 'wbgetentities',
            'format': 'json',
            'ids': '|'.join(qids),
            'props': 'labels|aliases|descriptions|claims'
        }
        response = requests.get(api_url, params=payload)

        print(response)


parser = argparse.ArgumentParser(
    description='Fixes labels for various usages.')
parser.add_argument('-s', help='source file', default='qids.txt')
parser.add_argument('-p', help='property', default='P1705')
args = parser.parse_args()

source = args.s
prop = args.p

f = open(source, 'r')
qids = f.read()
f.close()

print(qids)

# from SPARQLWrapper import SPARQLWrapper, JSON
import argparse
import wikidata


parser = argparse.ArgumentParser(
    description='Fixes labels for various usages.')
parser.add_argument('-s', help='source file', default='qids.txt')
parser.add_argument('-p', help='property', default='P1705')
args = parser.parse_args()

source = args.s
prop = args.p

qids = []
f = open(source, 'r')
for l in f:
    qid = l.strip()
    if wikidata.is_qid(qid):
        qids.append(qid)
    else:
        print('not a valid qid:' + qid)
f.close()

print(qids)

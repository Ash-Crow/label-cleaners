#!/usr/bin/env python3
from SPARQLWrapper import SPARQLWrapper, JSON
import validators
import requests
import json


#############
# Constants

__author__ = "Sylvain Boissel <sylvain@ashtree.eu>"

SPARQL_TIMEFORMAT = "%Y-%m-%dT%H:%M:%SZ"
WD_ROOT_URL = 'https://www.wikidata.org'
WD_BASE_URL = WD_ROOT_URL + '/wiki/'
WD_API_URL = WD_ROOT_URL + '/w/api.php'


###########
# Classes


class Item:
    """
    A Wikidata item
    """
    def __init__(self, identifier=""):
        if is_item_uri(identifier):
            self.entiry_uri = identifier
            self.qid = self.uri_to_qid()
            self.base_uri = self.get_base_uri()
        elif is_qid(identifier):
            self.qid = identifier.upper()
            self.entiry_uri = self.get_entity_uri()
            self.base_uri = self.get_base_uri()
        else:
            self.qid = ""
            self.entiry_uri = ""
            self.base_uri = ""

    def __str__(self):
        return self.qid

    def __repr__(self):
        return "wikidata.item({})".format(self.qid)

    def uri_to_qid(self):
        return self.uri.split('/')[-1].upper()

    def get_base_uri(self):
        return "{}{}".format(WD_BASE_URL, self.qid)

    def get_entity_uri(self):
        return "http://www.wikidata.org/entity/{}".format(self.qid)

    def getWikidataContent(self):
        """
        Retrieves the item content from Wikidata
        """

##################
# API calls
#


def getentities(qids, props='labels|aliases|descriptions|claims'):
    payload = {
        'action': 'wbgetentities',
        'format': 'json',
        'ids': '|'.join(qids),
        'props': props
    }
    response = requests.get(WD_API_URL, params=payload)

    return response


##################
# SPARQL Queries
#


def query_raw(query):
    """
    Queries WDQS and returns the result as a dictionary
    """
    endpoint = "https://query.wikidata.org/bigdata/namespace/wdq/sparql"
    sparql = SPARQLWrapper(endpoint)
    sparql.setQuery(query)

    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return results


def query_items(query, main_key="item"):
    """
    Makes a WDQS query and sorts the results.
    The "main_key" variable is expected to be a Wikidata item.
    """
    results = query_raw(query)
    all_items = []

    keys = results["head"]["vars"]

    if main_key not in keys:
        print("Error: Unkown key")
    else:
        keys.remove(main_key)
        for r in results["results"]["bindings"]:
            item = Item(r[main_key]['value'])
            item.query_results = []

            print(keys)
            for k in keys:
                if k in r:
                    value = r[k]['value']
                    if is_item_uri(value):
                        value = Item(value).uri_to_qid()
                        out = (k, value)
                    elif 'xml:lang' in r[k]:
                        out = (k, value, r[k]['xml:lang'])
                    else:
                        out = (k, value)

                    item.query_results.append(out)

            all_items.append(item)

            print(r[main_key]['value'])
            print("item: {}".format(str(item)))
            print("item: {}".format(item.query_results))

            pprint(r)
            print("==========")

        return all_items


##################
# Custom validators
#
@validators.validator
def is_qid(value):
    if not (isinstance(value, str) or isinstance(value, unicode)):
        print(type(value))
        return False
    elif value[0].lower() != 'q':
        return False
    else:
        return value[1:].isdigit()


@validators.validator
def is_item_uri(value):
    if validators.url(value):
        parts = value.split('/')
        if parts[2] == "www.wikidata.org" and is_qid(parts[-1]):
            return True
    return False


"""""""""""""""""
from pprint import pprint

myquery = #Cats
 #Cats
SELECT DISTINCT ?item ?item_label ?birthDate ?birthPlace ?image ?coords
WHERE {
  ?item wdt:P31 wd:Q146 .
  ?item wdt:P569 ?birthDate .
  ?item wdt:P19 ?birthPlace .
  OPTIONAL {
    ?item rdfs:label ?item_label .
    FILTER(LANG(?item_label) IN ("fr", "en")) .
  }
  OPTIONAL { ?item wdt:P18 ?image . }
  OPTIONAL { ?birthPlace wdt:P625 ?coords . }
}

results = query_raw(myquery)
pprint(results)
results = query_items(myquery)
pprint(results)
"""

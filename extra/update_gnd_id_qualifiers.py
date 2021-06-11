#!/usr/bin/python

import sys
import requests
import pywikibot
from pywikibot import pagegenerators as pg 

GND_ID = 'P227'
NAMED_AS = 'P1810'
STATED_AS = 'P1932'
RETRIEVED = 'P813'
SITE = pywikibot.Site('wikidata', 'wikidata')
REPO = SITE.data_repository()
SESSION = requests.Session()

def main(limit):
    query = 'SELECT ?item ?stated WHERE {' \
      '?item wdt:P31 wd:Q5.' \
      '?item p:P227 ?statement.' \
      '?statement pq:P1932 ?stated.' \
    '}'
    items = pg.WikidataSPARQLPageGenerator(query, site=REPO)

    count = 0
    for item in items:
        item_data = item.get()
        for claim in item_data['claims'][GND_ID]:
            for q in claim.qualifiers[STATED_AS]:
                updateQualifier(claim, q)
                count += 1

def updateQualifier(claim, qual):
    val = getTargetVal(claim.target)
    retrieved = True 
    print( '1 => %s' % val )
    if not val:
        val = qual.target
        retrieved = False
    print( '2 => %s' % val )
    print( '3 => %s' % qual.target)
    print( '4 => %s' % 'd')
    return

    claim.removeQualifier(qual, summary='')

    qualifier = pywikibot.Claim(REPO, NAMED_AS)
    qualifier.setTarget(val)
    claim.addQualifier(qualifier, summary='')

    if retrieved:
        retrieved = pywikibot.Claim(REPO, RETRIEVED)
        reference.setTarget(pywikibot.WbTime(date.today()) )
        claim.addSource(retrieved, summary='')

def getTargetVal(id):
    print(id)
    url = "https://hub.culturegraph.org/entityfacts/" + id

    val = None
    result = SESSION.get(url)
    if result.status_code == 200:
        res = result.json()
        if res['@type'] == 'person':
            p = res.get('prefix', None)
            val = '%s, %s' %(res['surname'], res['forename'])
            val = ('%s, %s' %(val, p)) if p else val

    return val


if __name__ == '__main__':
    limit = int(sys.argv[1])

    main(limit)
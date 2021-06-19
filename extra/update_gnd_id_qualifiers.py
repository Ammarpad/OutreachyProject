#!/usr/local/bin/python3

import sys
import requests
import pywikibot
from datetime import datetime
from pywikibot import pagegenerators as pg 

GND_ID = 'P227'
NAMED_AS = 'P1810'
STATED_AS = 'P1932'
RETRIEVED = 'P813'
SITE = pywikibot.Site('wikidata', 'wikidata')
REPO = SITE.data_repository()
SESSION = requests.Session()
entityfacts = 'https://hub.culturegraph.org/entityfacts/'
summary = '([[Wikidata:Requests for permissions/Bot/AmmarpadBot|update GND ID qualifier]])'

def main(limit):
    query = 'SELECT ?item ?stated WHERE {' \
      '?item wdt:P31 wd:Q5.' \
      '?item p:P227 ?statement.' \
      '?statement pq:P1932 ?stated.' \
    '}'
    items = pg.WikidataSPARQLPageGenerator(query, site=REPO)
    count = 0
    try:
        for item in items:
            item.get()
            for claim in item.claims[GND_ID]:
                for qual in claim.qualifiers[STATED_AS]:
                    updateQualifier(claim, qual)
                    count += 1

                    if count == limit:
                        raise StopIteration
    except StopIteration:
        print('Finished. %s items updated.' %count)
    
def updateQualifier(claim, qual):
    val = getTargetVal(claim.target)
    retrieved = True 

    if not val:
        val = qual.target
        retrieved = False

    qualifier = pywikibot.Claim(REPO, NAMED_AS)
    qualifier.setTarget(val)
    qualifier.hash = qual.hash
    claim.addQualifier(qualifier, summary=summary)

    if retrieved and (qual.id != qualifier.id):
        retrieved = pywikibot.Claim(REPO, RETRIEVED)
        now = datetime.now()
        date = dict(year=now.year,
                    month=now.month,
                    day=now.day)
        retrieved.setTarget(pywikibot.WbTime(**date))
        claim.addSource(retrieved)

def getTargetVal(id):
    val = None
    result = SESSION.get(entityfacts + id)
    if result.status_code == 200:
        res = result.json()
        if res['@type'] == 'person':
            pref = res.get('prefix', '')
            sname = res.get('surname', '')
            fname = res.get('forename', '')
            if not fname or (fname and sname == ''):
                return fname if fname else None

            val = '%s, %s' %(fname, sname)
            val = ('%s %s' %(val, pref)) if pref else val

    return val

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)

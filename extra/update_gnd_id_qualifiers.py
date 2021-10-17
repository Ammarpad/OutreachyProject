#!/usr/local/bin/python3

import sys
import pywikibot
from pywikibot import pagegenerators as pg
from requests.exceptions import ConnectionError, ReadTimeout

GND_ID = 'P227'
NAMED_AS = 'P1810'
STATED_AS = 'P1932'
SITE = pywikibot.Site('wikidata', 'wikidata')
REPO = SITE.data_repository()
summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot|update GND ID qualifier]])'

def main(limit):
    query = 'SELECT ?item ?stated WHERE {' \
      '?item wdt:P31 wd:Q5.' \
      '?item p:P227 ?statement.' \
      '?statement pq:P1932 ?stated.' \
    '}'

    items = pg.WikidataSPARQLPageGenerator(query, site=REPO)
    count = 0
    retries = 5
    try:
        for item in items:
            for claim in item.claims[GND_ID]:
                if STATED_AS in claim.qualifiers:
                    for qual in claim.qualifiers[STATED_AS]:
                        updateQualifier(claim, qual)

                        count += 1
                        if count == limit:
                            raise StopIteration
    except pywikibot.exceptions.APIError as e:
        print('APIError. %s items updated. (%s)' %(count, e))
    except StopIteration:
        print('Finished. %s items updated.' %count)
    
def updateQualifier(claim, qual):
    qualifier = pywikibot.Claim(REPO, NAMED_AS)
    qualifier.setTarget(qual.target)
    qualifier.hash = qual.hash
    claim.addQualifier(qualifier, summary=summary)

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)

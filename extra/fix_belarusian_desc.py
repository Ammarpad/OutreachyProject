#!/usr/local/bin/python3

import sys
import pywikibot
from pywikibot import pagegenerators 

def main(limit):
    language = 'be' # Belarusian
    summary = 'fix be description; атыкулаў -> артыкулаў'
    fixed_desc = 'спіс артыкулаў у адным з праектаў Вікімедыя'

    site = pywikibot.Site('wikidata', 'wikidata')
    data_repo = site.data_repository()
    query = 'SELECT * WHERE {' \
      'VALUES ?desc { "спіс атыкулаў у адным з праектаў Вікімедыя"@be } .' \
      '?item schema:description ?desc . ' \
    '}'
    items = pagegenerators.WikidataSPARQLPageGenerator(query, site=data_repo)

    count = 0
    for item in items:
        item_data = item.get()
        be_desc = item_data['descriptions'].get(language)
        if be_desc:
            item.editDescriptions({language: fixed_desc}, summary=summary)
            count += 1
            print(f'{count}. Fixed {item_data.title()}')

        if count == limit:
            break

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)
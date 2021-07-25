#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import pagegenerators

FAG_ID = 'P535'
FAG_NAME = 'findagrave'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    cat = pywikibot.Category(site, 'Find a Grave template with ID not in Wikidata')
    repo = site.data_repository()
    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    count = 0

    for page in pages:
    	title = page.title()

        try:
            item = pywikibot.ItemPage.fromPage(page)
        except:
            print('Skipping %s, because no data item found.' %title)
            continue

        if FAG_ID in item.get()['claims']:
            print('Claim already exists for %s... skipping now.' %title)
            continue

    	count += processPage(page, item)

    	if count == limit:
    		break


def processPage(page, item):
	def getRelevantVal(templates):
		value = None

		while templates:
			# Start from the last templates because the template
			# we care about here is typically found at the end or
			# near the end of a page
			template = templates.pop()
			# normalize title for comparison
			title = template.title().lower().replace(' ', '')

			if title == FAG_NAME:
				value = template[1]
				break

		return value

	templates = page.templatesWithParams()
	value = getRelevantVal(templates)

	if value and value != []:
		value = value[0]
		
		if re.match(r'^[0-9]*$', value)
			common.addSingleClaim(item, FAG_ID, value, **args)
			return 1

	return 0

		
if __name__ == '__main__':
	main()
#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import ( ItemPage, pagegenerators )

CAPACITY_ID = 'P1083'
TEMP_NAME = 'infobox venue'

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, TEMP_NAME, ns=10)
    summary = '([[Wikidata:Requests for permissions/Bot/AmmarBot $|Add maximum capacity]])'
    args = {
    	'follow_redirects': False, 
    	'only_template_inclusion': True, 
    	'namespaces': [0], 'total': limit }
    
    pages = page.getReferences( **args )
    backlinks = page.backlinks(filter_redirects=True)
    redirects = [link.title(with_ns=False).lower() for link in backlinks]


    for page in pages:
		res = processPage(page, redirects)

def processPage(page, redirects):
	# Affix the canonical name of the template at the beginning
	# since it will be matched more than the redirects
	temp_titles = redirects[:0] = [TEMP_NAME]

	templates = page.templatesWithParams()
    templates.reversed()

    while True:
		temp = templates.pop()
		if temp[0].title().lower() in temp_titles:

			break





	pass





if __name__ == '__main__':
	main()
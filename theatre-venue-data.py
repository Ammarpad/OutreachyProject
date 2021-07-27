#!/usr/local/bin/python3

import re
import sys
import common
import pywikibot
from pywikibot import ( ItemPage, pagegenerators )

CAPACITY_ID = 'P1083'
TEMP_NAME = 'Infobox venue'

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
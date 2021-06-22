#!/usr/local/bin/python3

import re

import pywikibot
import wikitextparser as parser
from pywikibot import pagegenerators
import base_import_script as import_script

PROP_ID = 'P69'
CAT = 'Ahmadu Bello University alumni'
LIST_PAGE = 'List_of_Ahmadu_Bello_University_alumni'
wiki = pywikibot.Site('en', 'wikipedia')

def main():

	pages = get_pages()

	for page in pages:
		pass


def get_pages():
	page = pywikibot.Page(wiki, LIST_PAGE)
	parsed = parser.parse(page.text)
	listItems = parsed.get_lists()

	pages = list()
	lines = list()

	for index in range(0, len(listItems)):
		items = listItems[index]
		lines.extend(items.items)

	for line in lines:
		title = parser.parse(line)
		links = title.wikilinks
		if not links:
			continue

		title = links[0].title
		page = pywikibot.Page(wiki, title)

		if page.exists:
			pages.append(title)

	return pages

if __name__ == '__main__':
	main()
#!/usr/bin/python

import re

import pywikibot
from pywikibot import pagegenerators
import base_import_script as import_script

MusicBrainz = 'P436'
REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

def do_import():
    cat = 'MusicBrainz release group not in Wikidata'
    en_wiki = pywikibot.Site('en', 'wikipedia')
    repo = en_wiki.data_repository()
    catObj = pywikibot.Category(en_wiki, cat)
    data = no_data_item = list()
    summary = 'Adding release-group id'

    pages = pagegenerators.CategorizedPageGenerator(catObj, recurse=False)
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print("Skipping %s, no data item found" % page.title())
            no_data_item.append(page.title())
            continue

        group_id = get_link(page)

        if group_id:
            data.append([group_id, data_item])
            print("Found %s for %s:" %(group_id, page.title()))
        else:
            print('There\'s a problem with %s' % page.title())

    if len(no_data_item):
        import_script.record_pages_without_items(no_data, 'missing-data-items-list-mb')

    result = import_script.add_claims_to_item(repo, data, MusicBrainz, summary=summary)

    print("Finished. Imported %s pages, %s were skipped" %(result['added'], result['skipped']))

def get_link(page):
    # Redirects
    temps = ('Template:MusicBrainz release-group', 'Template:Musicbrainz release-group',
        'Template:Musicbrainz release group', 'Template:MusicBrainz release ID group')
    
    templates = page.templatesWithParams()
    
    func = lambda t: t == 'Template:MusicBrainz release group' or t in temps
    
    link = None
    for t in templates:
        if func(t[0].title()):
            link = re.findall(REGEX, t[1][0])
            break

    return link[0] if link else link

if __name__ == '__main__':
    do_import()
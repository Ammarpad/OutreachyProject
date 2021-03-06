#!/usr/local/bin/python3

import common
import pywikibot
from pywikibot import pagegenerators

MusicBrainz = 'P436'
REGEX = r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

def doImport(limit):
    cat = 'MusicBrainz release group not in Wikidata'
    site = pywikibot.Site('en', 'wikipedia')
    catObj = pywikibot.Category(site, cat)
    data = list()
    no_data_item = list()
    summary = 'Adding release-group id'

    pages = pagegenerators.CategorizedPageGenerator(catObj, recurse=False)
    found = 0
    for page in pages:
        data_item = common.getDataItem(page, verbose=True)
        if data_item is None:
            no_data_item.append(page.title())
            continue

        group_id = getLink(page)

        if group_id:
            data.append([group_id, data_item])
            print('Found %s for %s:' %(group_id, page.title()))
            found += 1
        else:
            print("There's a problem with %s" % page.title())

        if found == limit:
            break

    common.recordPages(no_data_item, 'missing-data-items-list-mb')

    result = common.addMultipleClaims(repo, data, MusicBrainz, check_value=False, summary=summary)

    print('Finished. Updated %s items, %s were skipped' %(result['added'], result['skipped']))

def getLink(page):
    # Redirects
    temps = ('Template:MusicBrainz release-group', 'Template:Musicbrainz release-group',
        'Template:Musicbrainz release group', 'Template:MusicBrainz release ID group')
    
    templates = page.templatesWithParams()
    
    func = lambda t: t == 'Template:MusicBrainz release group' or t in temps
    
    link = None
    for t in templates:
        if func(t[0].title()):
            link = pywikibot.re.findall(REGEX, t[1][0])
            break

    return link[0] if link else link

if __name__ == '__main__':
    limit = int(sys.argv[1])
    doImport(limit)

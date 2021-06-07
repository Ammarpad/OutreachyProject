import pywikibot
from bs4 import BeautifulSoup
from pywikibot import pagegenerators
import base_import_script as import_script

OFFICIAL_WEBSITE_PROPERTY = 'P856'
URL_REGEX = r'https?://[^\s<>"]+|www\.[^\s<>"]+'

def do_import():
    cat = 'Official_website_not_in_Wikidata'
    en_wiki = pywikibot.Site('en', 'wikipedia')

    cat = pywikibot.Category(en_wiki, cat)

    pages = pagegenerators.CategorizedPageGenerator(cat, recurse=False)
    for page in pages:
        try:
            data_item = pywikibot.ItemPage.fromPage(page)
        except:
            print("Skipping {}, no data item found", page.title())
            no_data.append(page.title())
            continue

        website = extract_weblink(page)

    if len(no_data):
        import_script.record_pages_without_items(no_data, 'missing-data-items-list')

def extract_weblink(page):
    page_source = page.expand_text(True)
    html = BeautifulSoup(page_source)
    link = html.findAll('span', {'class':'url', 'class':'official-website'})

    if not items or len(items) != 1:
        return None

    return re.findall(URL_REGEX, link)[0]

if __name__ == '__main__':
    do_import()
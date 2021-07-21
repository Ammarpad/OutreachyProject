#!/usr/local/bin/python3

import re, os, io, sys
import common, pywikibot

ISBN_13 = 'P212'
ISBN_10 = 'P957'
OCLC_1D = 'P243'
PAGE_NUM_ID = 'P1104'
BOOK_TEMPLATE = 'Infobox book'
ISBN_ID = { 10: ISBN_10, 13: ISBN_13 }
ALL_PROPS = (PAGE_NUM_ID, OCLC_1D, ISBN_13, ISBN_10)
# For basic validation of structure for both ISBN- 10 and 13
RE_ISBN = re.compile(r'^(97(8|9))?\d{9}(\d|X)$', re.I)

def main(limit):
    site = pywikibot.Site('en', 'wikipedia')
    repo = site.data_repository()
    page = pywikibot.Page(site, BOOK_TEMPLATE, ns=10)

    pages = page.getReferences(follow_redirects=False,
                        only_template_inclusion=True,
                        namespaces=[0],
                        total=limit)

    # This does the heavy work...
    allData = getData(pages, limit)

    # Now push all to the repo, prop by prop
    for prop in ALL_PROPS:
        data = allData[prop]
        if data != []:
            result = common.addMultipleClaims(data, prop, check_value=False, summary='')
            print(f"Finished for {prop}. Updated {result['added']} items, {result['skipped']} were skipped")

def getPageNum(templates):
    page_num = getValueRaw(templates, 'pages')

    if page_num and page_num.isdigit():
        return page_num

    num = re.findall(r'\d+', page_num)
    if len(num) == 1:
        return num[0]
    else:
        # Multiple values, probably for different
        # editions, it's hard to programmatically
        # extract these from free-form string
        return None

def getISBN(templates):
    isbn = getValueRaw(templates, 'isbn')
    if isbn:
        isbn = isbn.strip()
        raw = isbn.replace('-', '')
        return isbn, ISBN_ID.get(len(raw), 0) if RE_ISBN.match(raw) else None

    return None

def getOCLC(templates):
    ocnum = getValueRaw(templates, 'oclc')
    if ocnum:
        ocnum = ocnum.strip()
        return ocnum if re.match(r'^\d{1,14}$', ocnum) else None

    return None

def getValueRaw(templates, name):
    for t in templates:
        if t[0] == BOOK_TEMPLATE:
            return t[1].get(name)

    return False

def checkClaims(claimIDs, page):
    """Checks the repo to find if any of or all
    of these claims already exist on the item"""
    try:
        item = page.data_item()
    except pywikibot.exceptions.NoPage:
        # Pretend it does if we don't even have data item
        return []

    res = list()
    for claimID in claimIDs:
        if claimID not in item.get()['claims']:
            res.append(claimID)

    return res, item

def getData(pages, limit):
    data = dict.fromkeys(ALL_PROPS, [])
    path = os.path.dirname(__file__) + '/__local__/P1104_titles.txt'
    count = 0

    with open(path, mode='a+') as file:
        file.seek(io.SEEK_SET)
        lines = file.readlines()
        titles = [t.strip() for t in lines]

        for page in pages:
            title = page.title()

            if title in titles:
                continue

            ids, item = checkClaims(ALL_PROPS, page):
            if ids == [] or ids[0] == []:
                continue

            temps = page.raw_extracted_templates
            for prop in ids[0]:
                val = extractValue(temps, temps)
                if res:
                    current = data.get(prop)
                    data.update({prop: current.append(val, item)})
                    count += 1

            if limit == count:
                break

    return data

def extractValue(p_id, temps):
    if p_id == PAGE_NUM_ID:
        return getPageNum(temps)
    elif p_id == OCLC_ID:
        return getPageNum(temps)
    elif p_id in (ISBN_13 ISBN_10)
        return getISBN(temps)

    return False

def sparql_query():
    """SPARQL query alternative"""
    return "SELECT ?item " \
    "WHERE " \
    "{" \
      "VALUES ?type {wd:Q571 wd:Q7725634} " \
      "?item wdt:P31 ?type " \
      "MINUS { ?item wdt:P1104 [] }"\
    "}"

if __name__ == '__main__':
    limit = int(sys.argv[1])
    main(limit)

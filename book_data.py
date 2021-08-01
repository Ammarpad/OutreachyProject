#!/usr/local/bin/python3

import re
import os
import io
import sys
import common
import pywikibot

ISBN_13 = 'P212'
ISBN_10 = 'P957'
OCLC_ID = 'P243'
PAGE_NUM_ID = 'P1104'
BOOK_TEMPLATE = 'Infobox book'
ISBN_PROPS = { 10: ISBN_10, 13: ISBN_13 }
ALL_PROPS = (PAGE_NUM_ID, OCLC_ID, ISBN_13, ISBN_10)
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

    if not page_num:
        return None

    if page_num.isdigit():
        return page_num

    num = re.findall(r'\d+', page_num)

    # Sometimes there'd be multiple values, probably
    # for different editions, it's hard to programmatically
    # extract these from free-form string.
    # So we will use it here only if there's a single value
    return num[0] if len(num) == 1 else None

def getISBN(templates):
    isbn = getValueRaw(templates, 'isbn')
    if isbn:
        isbn = isbn.strip()
        raw = isbn.replace('-', '')
        ntype = ISBN_PROPS.get(len(raw), False)

        if ntype and RE_ISBN.match(raw):
            return isbn, ntype

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
            return t[1].get(name, False)

    return False

def checkClaims(claimIDs, page):
    """
    Checks the repo to find if any of or all
    of these claims already exist on the item.
    This will also check if the item is of the
    right instance for the modifications
    """
    item = common.getDataItem(page)
    if item is None:
        # Pretend it does if we don't even have data item
        return [],[]

    claims = item.get()['claims']

    P31 = claims['P31'] if 'P31' in claims else []

    if len(P31):
        instance = P31[0].toJSON()
        i_item = instance['mainsnak']['datavalue']['value']['item']
        #'book (Q571)', 'version, edition, or translation (Q3331189)'
        if int(i_item.get('numeric-id')) not in (571, 3331189):
            return [],[]

    res = list()
    for claimID in claimIDs:
        if claimID not in data['claims']:
            res.append(claimID)

    return res, item

def getData(pages, limit):
    """
    Initialize `data` dict with the properties that we will work on.
    This dictionary will be returned with all the data collected so
    far, meticulously arranged in the following format:

        data = {
            prop1: [ [ val, item ], [ val, item ] ],
            prop2: [ [ val, item ], [ val, item ] ],
            prop3: [ [ val, item ], [ val, item ] ]
        }

    `val` are the actual values extracted from various operations on
    pages. Each val has corresponding data item object witch is where
    it belongs on the repo (the data item of the source wiki page).
    The prop key are the property ids where the data belong.

    """
    data = dict.fromkeys(ALL_PROPS, [])

    path = os.path.dirname(__file__) + '/__local__/P1104_titles.txt'
    count = 0

    with open(path, mode='a+') as file:
        file.seek(io.SEEK_SET)
        lines = file.readlines()
        titles = [t.strip() for t in lines]

        for page in pages:
            title = page.title()

            if title not in titles:
                continue

            ids, item = checkClaims(ALL_PROPS, page)
            if ids == [] or item == []:
                continue

            temps = page.raw_extracted_templates
            for prop in ids:
                res = extractValue(prop, temps)
                if res:
                    # Special handling for ISBN(13|10)
                    # We hold the prop value from point of extraction
                    if prop in ISBN_PROPS.keys():
                        res = res[0]
                        prop = res[1]

                    data[prop].append([res, item])
                    count += 1

            if limit == count:
                break

    return data

def extractValue(prop, temps):
    if prop == PAGE_NUM_ID:
        return getPageNum(temps)
    elif prop == OCLC_ID:
        return getOCLC(temps)
    elif prop in ISBN_PROPS.keys():
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

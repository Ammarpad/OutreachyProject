#!/usr/bin/env python3

"""
Set of common reusable functions
"""
import pywikibot
from datetime import datetime
from requests.exceptions import ReadTimeout
from pywikibot.exceptions import APIError, Error

SITE = pywikibot.Site('en', 'wikipedia')
REPO = SITE.data_repository()

def addMultipleClaims(items, prop_id, summary='', add_ref=True, check_value=True):
    """
    Push claims to the data repository, add reference to each claim
    if so requested, handle error and return a dictionary with the
    following keys:

    'added': The number of claims successfuly published
    'skipped': The number of claims which could not be saved
    due to duplication or other error (if any)
    'pages': the page obejcts (in case of futher procssing)

    @param items: List of [id, page]; add id to the data item of page
    @param prop_id: The property ID
    @param summary: Optional edit summary to use
    @param ref: Whether to add P143 as reference
    @param check_value: Whether the data type of value should
           be checked and converted where necessary.
    @return dictionary with the keys mentioned above
    """
    added = skipped = 0
    pages = list()

    for i, page in items:
        page_item = page
        if not isinstance(page_item, pywikibot.ItemPage):
            page_item = page.data_item()

        try:
            addSingleClaim(page_item, prop_id, i, summary, add_ref, check_value)
            pages.append(page)
            added += 1
        except (APIError, Error) as e:
            skipped += 1
            qid = page_item.title()
            print('Error: Adding claim to %s failed: %s' % (qid, str(e)))
        except ReadTimeout:
            skipped += 1
            print('Timeout error while working on %s [%s]' %(qid, str(e)))
            continue

    return {'added': added, 'skipped': skipped, 'pages': pages}

def addReference(item_id, claim_id, ref_type, value):
    """
    This adds new qualifier to an existing claim

    @param item_id: entity id where to do the work
    @param prop_id: the propety id of the claim to add qualifier on
    @param claim_id: the propety id of the claim (qualifier) to add
    @param ref_type: the ref form (reference URL, stated in, etc)
    @param value: value of the reference
    """
    item = pywikibot.ItemPage(REPO, item_id)
    claims = item.get()['claims']
    claim = claims.get(claim_id)[0] or None

    if not claim:
        return 0

    try:
        reference = pywikibot.Claim(REPO, ref_type)
        reference.setTarget(value)
        claim.addSource(reference, summary='Adding reference.')
        return 1
    except:
       return 0

def addQualifier(item_id, claim_id, prop_id, target):
    """
    This adds new qualifier to an existing claim

    @param item_id entity id where to do the work
    @param prop_id the propety id of the claim to add qualifier on
    @param claim_id the propety id of the claim (qualifier) to add
    @param target value of the claim
    """
    item = pywikibot.ItemPage(REPO, item_id)
    claims = item.get()['claims']
    claim = claims.get(claim_id)[0] or None

    if not claim:
        return 0

    try:
        qualifier = pywikibot.Claim(REPO, prop_id)
        qualifier.setTarget(target)
        claim.addQualifier(qualifier, summary='Adding a qualifier.')
        return 1
    except:
       return 0

def addSingleClaim(item, prop_id, value, summary, add_ref=False, check_value=True):
    """
    This adds new claim to an Item and handles datatype conversion
    based on the property where we are to add the claim.

    @param item entity id where to do the work or pywikibot.ItemPage object
    @param prop_id the propety id of the claim
    @param value The claim to add
    @param summary Edit summary
     @param check_value: Whether the data type of value should
           be checked and converted as necessary.
    @raises pywikibot.Error on unknown datatype
    """
    if check_value:
        value = convertValue(prop_id, value)

    claim = pywikibot.Claim(REPO, prop_id)
    claim.setTarget(value)

    if not isinstance(item, pywikibot.ItemPage):
        item = pywikibot.ItemPage(REPO, item)

    item.addClaim(claim, summary=summary)

    if add_ref:
        page = pywikibot.Page(SITE, 'English Wikipedia')
        ref_item = page.data_item()
        addReference(item.title(), prop_id, 'P143', ref_item)

    print('New claim saved!')
    return 1

def convertValue(prop_id, value):
    """
    Convert value to appropriate type to prepare for insertion

    @param prop_id
    @param value
    """
    datatype = pywikibot.PropertyPage(REPO, prop_id).type
    
    if datatype == 'wikibase-item':
        value = pywikibot.ItemPage(REPO, value)
    elif datatype == 'commonsMedia':
        commons = pywikibot.Site('commons', 'commons')
        value = pywikibot.FilePage(commons, value)
    elif datatype == 'globe-coordinate':
        value = pywikibot.Coordinate(value[0], value[1])
    elif datatype == 'quantity':
        value = pywikibot.WbQuantity(value, site=REPO)
    elif datatype == 'time':
        form = len(value.split())
        if form == 3:
            style = '%d %B %Y'
        elif form == 2:
            style = '%B %Y'
        else:
            style = '%Y'
        dt = datetime.strptime(value, style).isoformat()
        value = pywikibot.WbTime(dt)
    elif datatype == 'geo-shape':
        value = pywikibot.WbGeoShape(value)
    elif datatype == 'monolingualtext':
        value = pywikibot.WbMonolingualText(value[0], value[1])
    elif datatype == 'tabular-data':
        value = pywikibot.WbTabularData(value)
    elif datatype == 'url':
        url = value
        if 'https://' not in value and 'http://' not in value:
            value = 'https://' + value
        if not pwikibot.re.match(r'https?://[^\s<>"]+|www\.[^\s<>"]+', value):
            raise pywikibot.Error('Invalid URL: %s' % url)
    elif datatype in ['math', 'external-id', 'musical-notation']:
        value = str(value)
    else:
        raise pywikibot.Error('Unknown datatype: %s' % datatype)

    return value

def recordPages(titles, file_name):
    """
    Write list of titles to the file_name.
    Does nothing if the titles list is empty

    @param titles: List of titles to record
    @param file_name: Name of file to write to
    """
    if len(titles):
        with open(file_name, mode='w', encoding='utf-8') as file:
            for t in titles:
                file.write(t)

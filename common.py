#!/usr/bin/env python3

"""
Set of common reusable functions
"""

import pywikibot

def push_claims_to_item(items, prop_id, summary='', ref=True, check_value=True):
    """
    Push claims (in batch) to the data repository, add reference to each
    claim if so requested, handle error and return a dictionary with the
    following keys:

    'added': The number of claims successfuly published
    'skipped': The number of claims which could not be saved
    due to duplication or other error (if any)
    'pages': the page obejcts (in case of futher procssing)

    @param items: List of [id, page]; add id to the data item of page
    @param prop_id: The property ID
    @param summary: Optional edit summary to use
    @param ref: Whether to add P143 as reference
    @return dictionary with the keys mentioned above
    """
    added = skipped = 0

    if ref:
	    wiki = pywikibot.Site('en', 'wikipedia')
	    page = pywikibot.Page(wiki, 'English Wikipedia')
	    ref_item = page.data_item()
	    ref_id = 'P143' # imported from Wikimedia project
    
    pages = list()

    for i, page in items:
        if not isinstance(page, pywikibot.ItemPage):
            page_item = page.data_item()
        else:
            page_item = page

        qid = page_item.title()

        try:
            # Add the claim
            add_claim_to_item(repo, page_item, prop_id, i, summary, check_value)
            if ref:
    		    add_reference(repo, qid, prop_id, ref_id, ref_item)

            added += 1
            pages.append(page)
        except (pywikibot.Error, pywikibot.data.api.APIError) as e:
            skipped += 1
            print('Error: Adding claim to %s failed: %s' % (qid, str(e)))

    return {'added': added, 'skipped': skipped, 'pages': pages}

def add_reference(item_id, claim_id, ref_type, value):
    """
    This adds new qualifier to an existing claim
    @param item_id: entity id where to do the work
    @param prop_id: the propety id of the claim to add qualifier on
    @param claim_id: the propety id of the claim (qualifier) to add
    @param ref_type: the ref form (reference URL, stated in, etc)
    @param value: value of the reference
    """
    item = pywikibot.ItemPage(repo, item_id)
    claims = item.get()['claims']
    claim = claims.get(claim_id)[0] or None

    if not claim:
        return 0

    try:
        reference = pywikibot.Claim(repo, ref_type)
        reference.setTarget(value)
        claim.addSource(reference, summary='Adding reference.')
        return 1
    except ValueError:
       return 0

def add_claim_to_item(repo, item, prop_id, value, summary, check_value=True):
    """
    This adds new claim to an Item and handles datatype conversion
    based on the property where we are to add the claim.

    @param repo DataSite
    @param item entity id where to do the work or pywikibot.ItemPage object
    @param prop_id the propety id of the claim
    @param value The claim to add
    @param summary Edit summary
    @param check_value
    @raises pywikibot.Error on unknown datatype
    """
    if check_value:
    	value = get_value_for_property(prop_id, value)

    claim = pywikibot.Claim(repo, prop_id)
    claim.setTarget(value)

    if not isinstance(item, pywikibot.ItemPage):
        item = pywikibot.ItemPage(repo, item)

    item.addClaim(claim, summary=summary)
    print('New claim saved!')
    return 1

def get_value_for_property(prop_id, value):
	datatype = pywikibot.PropertyPage(repo, prop_id).type
    
    if datatype == 'wikibase-item':
        value = pywikibot.ItemPage(repo, value)
    elif datatype == 'commonsMedia':
        commons = pywikibot.Site('commons', 'commons')
        value = pywikibot.FilePage(commons, value)
    elif datatype == 'globe-coordinate':
        value = pywikibot.Coordinate(value[0], value[1])
    elif datatype == 'quantity':
        value = pywikibot.WbQuantity(value, site=repo)
    elif datatype == 'time':
        form = len(value.split())
        if form == 3:
            style = '%d %B %Y'
        elif form == 2:
            style = '%B %Y'b
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
            # ensure scheme exists to avoid errors
            value = 'https://' + value
        if not re.math(r'https?://[^\s<>"]+|www\.[^\s<>"]+', value):
            raise pywikibot.Error('Invalid URL: %s' % url)
    elif datatype in ['math', 'external-id', 'musical-notation']:
        value = str(value)
    else:
        raise pywikibot.Error('Unknown datatype: %s' % datatype)

    return value
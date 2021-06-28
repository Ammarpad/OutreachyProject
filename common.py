#!/usr/bin/env python3

"""
Set of common reusable functions
"""

import pywikibot



def push_claims_to_item(items, prop_id, summary='', ref=True):
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
            add_claim_to_item(repo, page_item, prop_id, i, summary)
            if ref:
    		    add_reference(repo, qid, prop_id, ref_id, ref_item)

            added += 1
            pages.append(page)
        except (pywikibot.Error, pywikibot.data.api.APIError) as e:
            skipped += 1
            print('Error: Adding claim to %s failed: %s' % (qid, str(e)))

    return {'added': added, 'skipped': skipped, 'pages': pages}

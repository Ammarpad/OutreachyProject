#!/usr/local/bin/python3

import re

import pywikibot
import base_import_script as import_script

PAGE_NUM_ID = 'P1104'

site = pywikibot.Site('en', 'wikipedia')
page = pywikibot.Page(site, 'Infobox book', ns=10)
pages = page.getReferences(follow_redirects=False,
                        only_template_inclusion = True,
                        namespaces=[0],
                        total=10)

def main():
    pass


def get_page_num(page):
    for t in page.raw_extracted_templates:
        if t[0] == 'Infobox book':
            page_num = t[1].get('pages')

            if page_num is None:
                return None
            elif page_num.isdigit():
                return page_num
            else:
                num = re.findall(r'\d+', page_num)
                if len(num) == 1
                    return num[0]
                else:
                    # Multiple numbers for different editions
                    # not sure how to programmatically extract
                    # these for now
                    return None

if __name__ == '__main__':
    main()

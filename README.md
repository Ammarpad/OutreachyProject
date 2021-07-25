## OOUTREACHY PROJECT
##### See [OutreachyProposal][1] for background.

This repository is a collection of python modules written as work for Outreachy internship with Wikimedia Foundation with guidance of [Mike Peel][mike], the mentor.

Development (is) being done with Python 3.8.0 and master branch of [Pywikibot package][pyw]. Some modules may requires additional libraries, where such is the case, is noted in the brief module note below.


0. **common.py**
	- This is a meta module that contains the base logic and generic functions that all 	the other modules can use to avoid code duplication. It facilatates converting value to approrriate data type for wikibase needs as well as pushing the collected data to the data repository (Wikidata)
1. **official\_website.py**
	- This module extracts official website links from Wikipedia article and add them to corresponding data item of the page on the repo. This module uses [BeautifulSoup library][2] apart from the standard requirments. It does not validate that the url is actually working, but it does ensure that it is valid URL in structure.
2. **twitter\_username.py**
	- This module primarily extracts Twitter usernames of subjects from Wikipedia page, or set of pages, and then use the username to extract its corresponding numeric id from Twitter. The username is then exported to Wikidata as [Twitter username][P2002] claim, and the numeric id as [Numeric id][P6552] qualifier
3. **mb\_release\_group\_data.py**
	- This module currently extracts and processes [MusicBrainz release group identifier][P436]
4. **lepindex-id.py**
	- This module extracts [LepIndex][3] (an dentifier for a Lepidoptera taxon in the UK Natural History Museum's 'Global Lepidoptera Names Index') from Wikipedia articles and stores them in the data repository. It can work with arbitrary page or set of pages (categorized) such as the set automatically generated by this [wikipedia category][4].
5. **book\_data.py**
    - This modules can be used to extract and export multiple value statements from wikipedia articles about books to Wikidata. Presently it can process a single page or list of pages and primarily extract either one, two or all of these: [OCLC number][P243], [ISBN number][Q33057] (both 10 and 13) as well as [Number of pages][P1104]. There's a basic validation for each value extracted to reduce chance of invalid values.
6. **power_stations.py**
7. **find\_a\_grave-id.py**
8. **Next**
9. **Next**
10. **Next**


[1]: https://github.com/Ammarpad/OutreachyProposal
[2]: https://pypi.org/project/beautifulsoup4/
[3]: https://www.nhm.ac.uk/our-science/data/lepindex/intro.html
[4]: https://en.wikipedia.org/wiki/Category:LepIndex_ID_not_in_Wikidata

[mike]: https://mikepeel.net
[pyw]: https://github.com/wikimedia/pywikibot
[Q33057]: https://www.wikidata.org/wiki/Q33057
[P436]: https://www.wikidata.org/wiki/Property:P436
[P243]: https://www.wikidata.org/wiki/Property:P243
[P1104]: https://www.wikidata.org/wiki/Property:P1104
[P6552]: https://www.wikidata.org/wiki/Property:P6552
[P2002]: https://www.wikidata.org/wiki/Property:P2002


## LICENSE
The code in this responsitory is made available under the [MIT LICENSE](LICENSE.md).

* _[Navigate interactively at sourcegraph](https://sourcegraph.com/github.com/Ammarpad/OutreachyProject/)_

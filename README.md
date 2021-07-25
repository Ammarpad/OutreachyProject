# OutreachyProject
##### See [OutreachyProposal](https://github.com/Ammarpad/OutreachyProposal) for background.


0. **common.py**
	- This is a meta module that contains generic functions that all 	the other modules can use to avoid code duplication. It 	facilatates converting value to approrriate data type as well as 	pushing the collected data to the data repository (Wikidata)
1. **official\_website.py**
	- This module extracts official website links from Wikipedia article and add them to corresponding data item of the page on the repo. This module uses [BeautifulSoup library](https://pypi.org/project/beautifulsoup4/) apart from the standard requirments. It does not validate that the url is actually working, but it does ensure that it is valid URL in structure.
2. **twitter\_username.py**
	- This modules 
3. **mb\_release\_group\_data.py**
4. **lepindex-id.py**
	- This module extracts LepIndex (an dentifier for a Lepidoptera taxon in the UK Natural History Museum's 'Global Lepidoptera Names Index') from Wikipedia articles and stores them in the data repository. It can work with arbitrary page or set of pages (categorized) such as the set automatically generated by this [wikipedia category](https://en.wikipedia.org/wiki/Category:LepIndex_ID_not_in_Wikidata).
5. **book\_data.py**
    - This modules can be used to extract and export multiple value statements from wikipeia articles about books to Wikidata.
6. **power_stations.py**
7. **find\_a\_grave-id.py**
8. **Next**
9. **Next**
10. **Next**


* _[Navigate interactively at sourcegraph](https://sourcegraph.com/github.com/Ammarpad/OutreachyProject/)_

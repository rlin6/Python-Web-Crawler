# Python-Web-Crawler
A parallelized implemention of a basic web crawler in Python3

Written by: Ricky Lin

Time Took: ~3 hours 

## How to Use 
All the libraries should be installed already with Python except requests and Beautiful Soup. To install those packages in the same environment as the program, enter 

`pip3 install bs4`

and 

`pip3 install requests`

in the terminal.

Then, to run the program, use

`python3 webcrawler.py`

The user will be prompted to enter the url of an website. Please type in the website name starting with http:// or https:// and include the '.' in the .com, .org, etc. 

## Tests 
I would like to first thank the creators of https://crawler-test.com for creating so many test cases to run my program against. 

Test 1: https://crawler-test.com/links/broken_links_internal: There are only internal links on this page, so the program should just print the page url and terminate:

https://crawler-test.com/links/broken_links_internal

Test 2: https://crawler-test.com/links/broken_links_external: There are only broken external links on this page, so the program should print the page url and those linked urls before terminating:

https://crawler-test.com/links/broken_links_external \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken1 \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken2 \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken3 \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken4 \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken5 
  
 Test 3: https://crawler-test.com/links/max_external_links: There are 13 absolute urls on this page, each leading to a known website. The first website crawled should include these websites: 

https://crawler-test.com/links/max_external_links \
&nbsp;&nbsp;&nbsp;&nbsp;http://deepcrawl.co.uk \
&nbsp;&nbsp;&nbsp;&nbsp;http://semetrical.com \
&nbsp;&nbsp;&nbsp;&nbsp;http://google.com \
&nbsp;&nbsp;&nbsp;&nbsp;http://bukowydwor.pl \
&nbsp;&nbsp;&nbsp;&nbsp;http://glenaholmmotopo.pl \
&nbsp;&nbsp;&nbsp;&nbsp;http://wyszehrad.pl \
&nbsp;&nbsp;&nbsp;&nbsp;http://momoweb.co.uk \
&nbsp;&nbsp;&nbsp;&nbsp;http://binarycat.co.uk \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org \
&nbsp;&nbsp;&nbsp;&nbsp;http://lolcats.com \
&nbsp;&nbsp;&nbsp;&nbsp;http://somerandomdomain.com \
&nbsp;&nbsp;&nbsp;&nbsp;http://robotto.org/broken \
&nbsp;&nbsp;&nbsp;&nbsp;http://bbc.co.uk
  
and subsequent crawls should have each of these websites as the page being visited, meaning they are not tabbed (too many to include all here). 

## Assumption 
The order of the web crawl may not reflect the order of the absolute urls on the webpage itself, due to the parallelization of the threads. I believe this will not affect the function of the program, so it is not much to pay for using threads and keeping the code simpler. 

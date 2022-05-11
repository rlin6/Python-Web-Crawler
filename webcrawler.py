from threading import Thread, Lock
from queue import Queue
import ssl
from urllib.request import Request, urlopen, URLError
from bs4 import BeautifulSoup


## On a high level, the web crawler works like so:

## 1. Add the website the user inputs to shared queue that every Crawler thread has access to.

## 2. In parallel, each Crawler thread will request a url to crawl from that shared queue,
## end the thread if there are no more urls to crawl

## 3. Each Crawler will take that url and retrieve all the urls on the HTML page.

## 4. The crawlers check every internal url to make sure that it is an absolute url and hasn't been visited before.

## 5. If it fulfills those conditions, the internal url will be added to the shared queue and an output queue
## for another Crawler to process its own internal urls

## 6. Concurrently running with the Crawler threads are Writer threads, which reads from the output queue and prints the
## the websites crawled and its linked urls as the web crawl is happening 

class Crawler(Thread):

    # constructor for a Crawler 
    def __init__(self, initial_url, urls_to_crawl, printing_crawl, already_visited, url_lock):

        Thread.__init__(self)                       # default Thread constructor 
        self.initial_url = initial_url              # takes the url that the user inputs

        self.urls_to_crawl = urls_to_crawl          # the shared queue between Crawlers that contains the urls that still needs to be crawled

        self.printing_crawl = printing_crawl        # the output queue between Crawlers and Writers, where
                                                    # Crawlers put all the crawled pages and linked urls for Writers to print out

        self.already_visited = already_visited      # set that tracks all the pages already crawled 

        self.url_lock = url_lock                    # a global Thread lock for cases when we want to prevent
                                                    # Crawlers from accessing the queue at the same time


    # infinite loop that each Crawler is running until there are no more pages left to crawl in the shared queue
    def run(self):

        # create an ssl context object so that we can crawl the pages using ssl handshake
        my_ssl = ssl.create_default_context()
        my_ssl.check_hostname = False
        my_ssl.verify_mode = ssl.CERT_NONE

        while True:

            # lock the shared queue so that only one Crawler can take an url from the queue at one time
            self.url_lock.acquire()
            link = self.urls_to_crawl.get()
            self.url_lock.release()

            # if there are no more links left to crawl, we are done and end the loop
            if link is None:
                print("The crawl has finished")
                break

            # then, we only extract the internal links if this is a new page not yet crawled
            if link not in self.already_visited:
                try:
                    # since we are going crawl this page now, we record that we have crawled it
                    self.already_visited.add(link) 

                    # use Request and BeautifulSoup to get HTML page of the link  
                    req = Request(link, headers= {'User-Agent': 'Mozilla/5.0'})
                    response = urlopen(req, context=my_ssl)
                    soup = BeautifulSoup(response.read(),"html.parser")

                    self.internal_urls = set() # ensure that there are no duplicate links added to queue

                    self.printing_crawl.put(link + "\n") # add link to the output queue to print 
                    
                    # recover all the links in <a href> tags
                    for a_tag in soup.find_all('a'):
                        url = a_tag.get('href')

                        if (url and not (url is None) and                                       # check that the link contains something  
                        url not in self.already_visited and url not in self.internal_urls and   # check that it has not been visited bfore
                        url.startswith('http') and '.' in url):                                 # check that it is an absolute url

                            # add the internal url to the shared queue to crawl later and the output queue to print out
                            self.internal_urls.add(url)
                            self.urls_to_crawl.put(url)
                            self.printing_crawl.put("\t" + url + "\n")

                except URLError as e:
                    continue

                # signal that the Crawler has finished crawling a page
                finally:
                    self.urls_to_crawl.task_done()

class Writer(Thread):

    # construct a Writer thread that prints results from an output queue
    def __init__(self, printing_crawl):
        Thread.__init__(self)
        self.printing_crawl = printing_crawl

    # infinite loop that prints the results of the crawl into the console while
    # this is still output to be printed
    def run(self):
        while True:
            try:
                url = self.printing_crawl.get()
                if url is None:
                    break
                print(url, end='')

            finally:
                self.printing_crawl.task_done()

                

if __name__=='__main__':

    # we ask for user input on the site they want to begin the crawl from 
    initial_url = input("Please Enter Website to Crawl > ")

    number_of_threads = 10 # we will be using 10 threads

    # create the shared queue and add the inputted url 
    urls_to_crawl = Queue()
    urls_to_crawl.put(initial_url)

    # initialize the rest of the parameters
    printing_crawl = Queue()
    already_visited = set()
    url_lock = Lock()


    # start all the Writer threads, ready to print the results of the crawl
    for i in range(number_of_threads):
        writer = Writer(printing_crawl)
        writer.start()

    # start all the Crawler threads and start the web crawl 
    for i in range(number_of_threads):
        crawler = Crawler(initial_url = initial_url, 
                          urls_to_crawl = urls_to_crawl,
                          printing_crawl = printing_crawl,
                          already_visited = already_visited,
                          url_lock = url_lock)
        crawler.start()

    # terminate both the Crawlers and Writers once they are done 
    urls_to_crawl.join()
    printing_crawl.join()
    


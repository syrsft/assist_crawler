# -*- coding: utf-8 -*-

import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer, StopParsing
from urlparse import urlparse
from threading import Thread
import mimetypes


# IMHO, Crawl depth 2 is enough for a non-professional tool like this
MAX_CRAWL_DEPTH = 2


# Worker thread.
# Visits a web page and extract URLS in it
class CrawlerThread(Thread):
    def __init__(self, visit_url, target_url):
        """
        :param visit_url: URL of the web page to visit
        :param target_url: URL of the crawl target
        """
        Thread.__init__(self)
        self.visit_url = visit_url
        self.target_url = target_url
        self.found_urls = None

    def run(self):
        http = httplib2.Http()
        headers = {'user-agent': 'Mozilla/5.0 AppleWebKit/537.36 Chrome/62.0.3202.94 Safari/537.36'}
        status, response = http.request(self.visit_url, 'GET', None, headers)

        url_parsed = urlparse(self.target_url)
        scheme = url_parsed.scheme
        host = url_parsed.hostname

        self.found_urls = []

        # get all "a href" URLs
        try:
            urls = BeautifulSoup(response, parseOnlyThese=SoupStrainer('a', {'href': True})).contents
        except (UnicodeEncodeError, StopParsing):
            return

        if urls is None:
            return

        for url in urls:
            href = url['href']
            # modify href if necessary
            if href.startswith('//'):
                href = scheme + ':' + href
            elif href.startswith('/'):
                href = scheme + '://' + host + href
            # check link type whether it is page or file
            link_type, _ = mimetypes.guess_type(href, False)
            if link_type is None or link_type is 'text/html':
                if href != self.target_url and href.startswith(self.target_url) and href not in self.found_urls:
                    self.found_urls.append(href)

    def join(self):
        Thread.join(self)
        return self.found_urls


# Crawl Manager
# Manages thread creation for web page visiting and collecting found URLs
class Crawler(object):
    def __init__(self):
        self.found_urls = []
        self.visited_urls = []

    def crawl(self, target_url):
        self.found_urls[:] = []
        self.visited_urls[:] = []
        self.found_urls.append(target_url)

        level = 1
        while True:
            # create crawler threads
            threads = []
            for url in self.found_urls:
                if url not in self.visited_urls:
                    print "Creating thread for {0}".format(url)
                    t = CrawlerThread(url, target_url)
                    threads.append(t)
                    self.visited_urls.append(url)
                    t.start()

            # collect results
            for t in threads:
                urls = t.join()
                if urls is None:
                    continue
                for url in urls:
                    if url not in self.found_urls:
                        self.found_urls.append(url)

            level += 1
            if level > MAX_CRAWL_DEPTH:
                break

        self.found_urls.sort()

        return self.found_urls

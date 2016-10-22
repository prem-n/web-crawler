from __future__ import division
import urllib2
import re
from pymongo import MongoClient

class MongoDB(object):
    username = 'admin'
    password = 'admin'
    uri = 'mongodb://<dbuser>:<dbpassword>@ds019668.mlab.com:19668/premmongo'
    client = None
    def create_mongo_client(self):
        self.uri.replace('dbuser', self.username)
        self.uri.replace('dbpassword', self.password)
        self.client = MongoClient(self.uri)

class Wikipedia(object):
    RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
    HOME_PAGE = "https://en.wikipedia.org"
    PHILOSOPHY = "https://en.wikipedia.org/wiki/Philosophy"
    positive = 0
    negative = 0
    total_path_length = 0
    number_of_pages = 0

    class Hyperlink():
        next_url = None
        to_philosophy = None

        def __init__(self, next_url, to_philosophy):
            self.next_url = next_url
            self.to_philosophy = to_philosophy

        def  __str__(self):
            return str([self.next_url, self.to_philosophy])

    HYPERLINKS = dict()

    def print_hyperlinks(self):
        for key, value in self.HYPERLINKS.iteritems():
            print key, value


    def is_valid_hyperlink(self, hyperlink, paragraph):
        """

        :param hyperlink: The hyperlink which needs to be validated.
        :param paragraph: The paragraph from which the hyperlink was extracted from.
        :return: Returns True if the hyperlink was valid
        """

        def is_cite_note(hyperlink):
            """

            :param hyperlink: The hyperlink to be verified.
            :return: Returns True if this is a cite_note
            """
            if 'cite_note' in hyperlink:
                return True
            else:
                return False

        def check_parenthesis(hyperlink, paragraph):
            """

            :param hyperlink: The hyperlink to be verified.
            :param paragraph: The paragraph within which the hyperlink is to be searched.
            :return: Returns True if the hyperlink is not within a parenthesis.
            """
            begin_index = paragraph.find(hyperlink)
            parenthesis_count = 0
            for i in range(0, begin_index):
                if paragraph[i] == '(':
                    parenthesis_count += 1
                elif paragraph[i] == ')':
                    parenthesis_count -= 1

            if parenthesis_count > 0:
                return False
            else:
                return True

        def is_red_link(hyperlink):
            if 'redlink' in hyperlink:
                return True

        def is_image(hyperlink):
            if '.svg' in hyperlink:
                return True

        def is_external_text(hyperlink):
            if 'class="ext' in hyperlink:
                return True

        if is_cite_note(hyperlink):
            return False
        if not check_parenthesis(hyperlink, paragraph):
            return False
        if is_red_link(hyperlink):
            return False
        if is_image(hyperlink):
            return False
        if is_external_text(hyperlink):
            return False
        if self.has_symbols(hyperlink):
            return False

        return True

    def has_symbols(self, hyperlink):
        url = self.get_url_from_link(hyperlink)
        if not url:
            return True
        if '<' in url or '>' in url or '.ogg' in url or 'IPA_for' in url:
            return True
        else:
            return False

    def get_url_from_link(self, link):
        if 'class=' in link:
            suffix = re.findall('href="(.*?)" class=(.*?) title=(.*?)', link)
        else:
            suffix = re.findall('href="(.*?)" title=(.*?)', link)
        #print 'link=' + link
        #print 'suffix=' + str(suffix)
        try:
            return self.HOME_PAGE + suffix[0][0]
        except IndexError:
            return None

    def get_first_hyperlink(self, paragraph):
        """

        :param paragraph: The paragraph which needs to be searched.
        :return: Searches for a valid hyperlink in the paragraph.
        """
        hyperlinks = re.findall(r'<a(.*?)</a>', paragraph)
        for hyperlink in hyperlinks:
            #print hyperlink
            if self.is_valid_hyperlink(hyperlink, paragraph):
                return hyperlink
        return None

    def get_paragraphs(self, page):
        """

        :param page: The contents of a web page
        :return: Extract and return all the paragraphs.
        """
        paragraphs = re.findall(r'<p>(.*?)</p>', page)
        return paragraphs

    def get_link_from_page(self, page):
        """

        :param page: The contents of a web page
        :return: Return the first valid hyperlink from the page
        """
        paragraphs = self.get_paragraphs(str(page))
        # print paragraphs
        for paragraph in paragraphs:
            first_hyperlink = self.get_first_hyperlink(str(paragraph))
            if first_hyperlink:
                return self.get_url_from_link(first_hyperlink)

    def get_page_from_url(self, url):
        """

        :param url: The URL of the web page
        :return: The contents of the web page
        """
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.HTTPError:
            self.get_page_from_url(url)

    def get_random_url(self):
        page = self.get_page_from_url(self.RANDOM_URL)
        url = re.findall(r'<link rel="canonical" href="(.*?)"/>', page)
        return url.pop()

    def crawl(self, num_of_pages):
        self.number_of_pages = num_of_pages
        for i in range(num_of_pages):
            url = self.get_random_url()
            #url = 'https://en.wikipedia.org/wiki/Mississippi'
            visited = []
            count = 0
            print i+1," ) ", url,
            reached = False
            while url not in visited and url != self.PHILOSOPHY:
                visited.append(url)
                if url in self.HYPERLINKS:
                    #url = self.HYPERLINKS[url]
                    count += self.HYPERLINKS[url].to_philosophy
                    new_url = self.HYPERLINKS[url]
                    while new_url.next_url != self.PHILOSOPHY:
                        #print new_url.next_url
                        new_url = self.HYPERLINKS[new_url.next_url]
                    #print self.PHILOSOPHY
                    self.total_path_length += count
                    self.positive += 1
                    reached = True
                    break
                else:
                    page = self.get_page_from_url(url)
                    new_url = self.get_link_from_page(page)
                    if not new_url:
                        self.negative += 1
                        reached = True
                        count = 0
                        break
                    #print new_url
                    #self.HYPERLINKS[url] = new_url
                    url = new_url
                count += 1
            visited.append(url)

            if reached:
                print ' ==> Path length = ' + str(count)
                continue

            if url == self.PHILOSOPHY:
                print ' ==> Path length = ' + str(count)
                self.positive += 1
                self.total_path_length += count
                for j in range(len(visited)-1):
                    if visited[j] != self.PHILOSOPHY:
                        h = self.Hyperlink(visited[j+1], count-j)
                        self.HYPERLINKS[visited[j]] = h
            else:
                print ' ==> Path length = ' + str(count)
                self.negative += 1

        print 'Positive = ' + str(self.positive), 'Negative = ' + str(self.negative)

    def print_stats(self):
        percent = 100 * self.positive / self.number_of_pages
        print str(percent) + '% of pages often lead to philosophy.'
        distribution = int(self.total_path_length / self.positive)
        print 'The distribution of path length for ' + str(self.number_of_pages) + ' pages is ' + str(distribution)

def main():
    #num_of_pages = 500
    #wiki = Wikipedia()
    #wiki.crawl(num_of_pages)
    #wiki.print_stats()
    #print wiki.get_random_url()

    m = MongoDB()
    m.create_mongo_client()
    #m.client.connection.api.authenticate("admin", "admin")
    my_wiki = m.client.wiki
    print m.client
    print my_wiki
    #table = db['crawler']
    record = {'url' : 'https://en.wikipedia.org/wiki/Mississippi',
              'next_url' : 'https://en.wikipedia.org/wiki/U.S._state',
              'to_philosophy' : 10}
    #id = m.client.db.crawler.insert(record)
    #print id

main()


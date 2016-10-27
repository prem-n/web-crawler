from __future__ import division
import urllib2
import re
import numpy


class Wikipedia(object):
    class Hyperlink():
        next_url = None
        to_philosophy = None

        def __init__(self, next_url, to_philosophy):
            self.next_url = next_url
            self.to_philosophy = to_philosophy

        def  __str__(self):
            return str([self.next_url, self.to_philosophy])

    RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
    HOME_PAGE  = "https://en.wikipedia.org"
    PHILOSOPHY = "https://en.wikipedia.org/wiki/Philosophy"
    hyperlinks = dict()
    positive = 0
    negative = 0
    total_path_length = 0
    number_of_pages = 0
    verbose = None

    def __init__(self, number_of_pages, verbose):
        self.number_of_pages = number_of_pages
        self.verbose = verbose

    def __is_valid_hyperlink(self, hyperlink, paragraph):
        """
        Returns True if the hyperlink is valid.

        :param hyperlink: The hyperlink which needs to be validated
        :param paragraph: The paragraph from which the hyperlink was extracted
        :return: Bool
        """

        def is_cite_note(hyperlink):
            """
            Returns True if the hyperlink is a cite note.

            :param hyperlink: The hyperlink to be verified
            :return: Bool
            """
            if 'cite_note' in hyperlink:
                return True
            else:
                return False

        def check_parenthesis(hyperlink, paragraph):
            """
            Returns True if the hyperlink is not within a parenthesis.

            :param hyperlink: The hyperlink to be verified
            :param paragraph: The paragraph within which the hyperlink is to be
                              searched
            :return: Bool
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
            """
            Returns True if the hyperlink is a red link.

            :param hyperlink: The hyperlink to be verified
            :return: Bool
            """
            if 'redlink' in hyperlink:
                return True

        def is_image(hyperlink):
            """
            Returns True if the hyperlink is a reference to an image file.

            :param hyperlink: The hyperlink to be verified
            :return: Bool
            """
            if '.svg' in hyperlink:
                return True

        def is_external_text(hyperlink):
            """
            Returns True if the hyperlink texts you to a page outside Wikipedia.

            :param hyperlink: The hyperlink to be verified
            :return: Bool
            """
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
        if self.__has_symbols(hyperlink):
            return False

        return True

    def __has_symbols(self, hyperlink):
        """
        Returns True if the hyperlink has some invalid text.

        :param hyperlink: The hyperlink to be verified
        :return: Bool
        """
        url = self.__get_url_from_link(hyperlink)
        if not url:
            return True
        if '<' in url or '>' in url or '.ogg' in url or 'IPA_for' in url:
            return True
        else:
            return False

    def __get_url_from_link(self, link):
        """
        Constructs an URL from the HTML source.

        :param link: The raw HTML source code
        :return: String
        """
        if 'class=' in link:
            suffix = re.findall('href="(.*?)" class=(.*?) title=(.*?)', link)
        else:
            suffix = re.findall('href="(.*?)" title=(.*?)', link)
        try:
            return self.HOME_PAGE + suffix[0][0]
        except IndexError:
            return None

    def __get_first_hyperlink(self, paragraph):
        """
        Returns the first valid hyperlink found in a paragraph.

        :param paragraph: The paragraph which needs to be searched
        :return: String
        """
        hyperlinks = re.findall(r'<a(.*?)</a>', paragraph)
        for hyperlink in hyperlinks:
            if self.__is_valid_hyperlink(hyperlink, paragraph):
                return hyperlink
        return None

    def __get_paragraphs(self, page):
        """
        Extracts the text present within paragraph tags in the HTML source code.

        :param page: The raw HTML source code
        :return: List
        """
        paragraphs = re.findall(r'<p>(.*?)</p>', page)
        return paragraphs

    def __get_link_from_page(self, page):
        """
        Returns the first valid hyperlink from the raw HTML source code.

        :param page: The raw HTML source code
        :return: String
        """
        paragraphs = self.__get_paragraphs(str(page))
        # print paragraphs
        for paragraph in paragraphs:
            first_hyperlink = self.__get_first_hyperlink(str(paragraph))
            if first_hyperlink:
                return self.__get_url_from_link(first_hyperlink)

    def __get_page_from_url(self, url):
        """
        Extract the raw HTML source code from an URL.

        :param url: The URL of the web page
        :return: The contents of the web page
        """
        try:
            request = urllib2.Request(url)
            response = urllib2.urlopen(request)
            page = response.read()
            return page
        except urllib2.HTTPError:
            self.__get_page_from_url(url)

    def __get_random_url(self):
        """
        Returns a random url from Wikipedia.

        :return: String
        """
        page = self.__get_page_from_url(self.RANDOM_URL)
        url = re.findall(r'<link rel="canonical" href="(.*?)"/>', page)
        return url.pop()

    def print_stats(self):
        """
        Prints the stats of the previous crawl.

        :return: None
        """
        print 'Total number of pages crawled = ' + str(self.number_of_pages)
        print 'Number of pages reaching Philosophy = ' + str(self.positive)
        print 'Number of pages not reaching Philosophy = ' + str(self.negative)

        percent = 100 * self.positive / self.number_of_pages
        print str(percent) + '% of pages often lead to philosophy.'

        mean = int(self.total_path_length / self.positive)
        print 'The mean of the path length for ' + \
              str(self.number_of_pages) + ' pages is ' + str(mean)

        median = int(numpy.median(numpy.array(self.positive)))
        print 'The median of the path lengths for ' + \
              str(self.number_of_pages) + ' pages is ' + str(median)



    def crawl(self):
        """
        Crawls through Wikipedia till the page Philosophy is reached.

        :return: None
        """
        for i in range(self.number_of_pages):
            url = self.__get_random_url()
            visited = []
            count = 0
            print str(i+1) + ") " + url,
            reached = False
            while url not in visited and url != self.PHILOSOPHY:
                visited.append(url)
                if url in self.hyperlinks:
                    count += self.hyperlinks[url].to_philosophy
                    new_url = self.hyperlinks[url]
                    while new_url.next_url != self.PHILOSOPHY:
                        if self.verbose:
                            print new_url.next_url
                        new_url = self.hyperlinks[new_url.next_url]
                    if self.verbose:
                        print self.PHILOSOPHY
                    self.total_path_length += count
                    self.positive += 1
                    reached = True
                    break
                else:
                    page = self.__get_page_from_url(url)
                    new_url = self.__get_link_from_page(page)
                    if not new_url:
                        self.negative += 1
                        reached = True
                        count = 0
                        break
                    if self.verbose:
                        print new_url
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
                        self.hyperlinks[visited[j]] = h
            else:
                print " ==> Doesn't reach Philosophy"
                self.negative += 1

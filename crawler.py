import urllib2
import re
from bs4 import BeautifulSoup

RANDOM_URL = "https://en.wikipedia.org/wiki/Special:Random"
HOME_PAGE  = "https://en.wikipedia.org"
PHILOSOPHY = "https://en.wikipedia.org/wiki/Philosophy"

def check_paranthesis(solution, line):
    pattern = '(<a' + solution + '</a>)'
    #TODO: Need to fix Hyperlinks within brackets far off.
    #pattern = r'\(.*' + re.escape(solution) + r'.*\)'
    #match = re.findall(pattern, line)
    #print line
    #if match:
    #    return False
    #else:
    #    return True
    if pattern in line:
        return False
    else:
        return True

def check_solution(solution, line):
    if not check_paranthesis(solution, line):
        return False
    return True

def get_first_hyperlink(line):
    hyperlinks = re.findall(r'<a(.*?)</a>', line)
    for hyperlink in hyperlinks:
        if check_solution(hyperlink, line):
            return hyperlink
    return None

def get_page_from_url(url):
    request = urllib2.Request(url)
    response = urllib2.urlopen(request)
    page = response.read()
    return page
    
def get_paragraphs(page):
    paragraphs = re.findall(r'<p>(.*?)</p>', page)
    return paragraphs
    
def get_random_article():
    return get_page_from_url(RANDOM_URL)
    
def get_link_from_page(page):
    paragraphs = get_paragraphs(str(page))
    #print paragraphs
    for paragraph in paragraphs:
        first_hyperlink = get_first_hyperlink(str(paragraph))
        if first_hyperlink:
            return first_hyperlink

def get_url_from_link(link):
    print link
    suffix = re.findall('href="(.*?)" title=(.*?)', link)
    return HOME_PAGE + suffix[0][0]

def main():
    visited = []
    url = 'https://en.wikipedia.org/wiki/Art'
    #url = 'https://en.wikipedia.org/wiki/Physics'
    #while url not in visited and url != PHILOSOPHY:
    #    visited.append(url)
    #    page = get_page_from_url(url)
    #    link = get_link_from_page(page)
    #    url = get_url_from_link(link)
    page = get_page_from_url(url)
    print get_link_from_page(page)
        
    
    if url == PHILOSOPHY:
        print 'yes'

main()
#print get_random_article()


import urllib2
import re

url = 'http://pythonprogramming.net/parse-website-using-regular-expressions-urllib/'

req = urllib2.Request(url)
resp = urllib2.urlopen(req)
respData = resp.read()

paragraphs = re.findall(r'<p>(.*?)</p>',str(respData))

for eachP in paragraphs:
    print(eachP)
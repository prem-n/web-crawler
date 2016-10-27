# web-crawler
A Web crawler which can crawl through web pages, download and parse data from them. Currently it is specialized for Wikipedia. 

Crawls through Wikipedia starting from a random article till the path
reaches PHILOSOPHY page. Terminates if there is a loop or a dead-end.
This process is repeated 'n' times, by default 10 and gives a stat of the
mean and median distribution of the path lengths.

Each URL is represented as a Hyperlink object. Each Hyperlink object contains
the path length from this page to PHILOSOPHY. This is used to optimize the
path length computations for random pages by re-using path lengths from visited
pages.

Candidate solutions are validated by checking if the hyperlinks are valid.
Some of the hyperlinks which are italicized or present inside parenthesis are
invalid. These candidate solutions are discarded and the next candidate solution
is evaluated.

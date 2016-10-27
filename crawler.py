import argparse
from wiki import Wikipedia


def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-n', type=int, default=10,
                        help='The number of pages to be crawled')
    parser.add_argument('-v', '--verbose', dest='v', default=None,
                        help='Verbose mode to look at more detailed execution steps.')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    wiki = Wikipedia(args.n, args.v)
    wiki.crawl()
    wiki.print_stats()

if __name__ == "__main__":
    main()

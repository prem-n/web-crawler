import argparse
from wiki import Wikipedia


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Crawls through wikipedia in search of philosophy.')
    parser.add_argument('-n', type=int, default=10,
        help='The number of pages to be crawled')
    parser.add_argument('--verbose', action='store_true',
        help='Verbose mode to look at more detailed execution steps.')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    wiki = Wikipedia(args.n, args.verbose)
    wiki.crawl()
    wiki.print_stats()

if __name__ == "__main__":
    main()

#!/usr/bin/env python

"""
The main driver script for the wiki crawler.

Crawls through Wikipedia starting from a random article till the path
reaches PHILOSOPHY page. Terminates if there is a loop or a dead-end.
This process is repeated 'n' times, by default 10 and gives a stat of the
mean and median distribution of the path lengths.

Author     : Prem Nagarajan
Created on : 20161026

"""

import argparse
from wiki import Wikipedia


def parse_arguments():
    """
    Parses and returns the command line arguments.
    
    :return: List
    """
    parser = argparse.ArgumentParser(
        description='Crawls through wikipedia in search of philosophy.')
        
    parser.add_argument('-n', type=int, default=10,
        help='The number of pages to be crawled')
        
    parser.add_argument('--verbose', action='store_true',
        help='Verbose mode to look at more detailed execution steps.')
        
    args = parser.parse_args()
    return args


def main():
    """
    The main method of execution.
    
    :return: None
    """
    args = parse_arguments()
    wiki = Wikipedia(args.n, args.verbose)
    wiki.crawl()
    wiki.print_stats()


if __name__ == "__main__":
    main()

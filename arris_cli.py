#!/usr/bin/env python

# CLI frontend to Arris modem stat scraper library arris_scraper.py

import argparse
import arris_scraper
import json
import pprint

default_url = 'http://192.168.100.1/cgi-bin/status_cgi'

parser = argparse.ArgumentParser(description='CLI tool to scrape information from Arris cable modem status pages.')
parser.add_argument('-f',
                    '--format',
                    choices=['ascii', 'json', 'pprint'],
                    default='ascii', dest='output_format',
                    help='output format')
parser.add_argument('-u',
                    '--url',
                    default=default_url,
                    help='url of modem status page')
args = parser.parse_args()

if args.output_format == 'ascii':
    print("ASCII output not yet implemented")
elif args.output_format == 'json':
    result = arris_scraper.get_status(args.url)
    print(json.dumps(result))
elif args.output_format == 'pprint':
    result = arris_scraper.get_status(args.url)
    pprint.pprint(result)
else:
    print("How in the world did you get here?")
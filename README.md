# Arris Cable Modem Scraper

Python scripts relating to scraping data from the web interface of an Arris
CM820 cable modem and likely many similar models.

The scraper library contained in "arris_scraper.py" depends on Requests and
BeautifulSoup to do its thing.

The CLI client "arris_cli" currently supports JSON and Python "pprint" style
output.  An ASCII table output format similar to MySQL's CLI is planned.

To use the test pages you currently need to make whichever one you'd like to
use appear as "status_cgi" or whatever is appropriate for the page being
tested.  The base can be whatever you want, but the end is currently
hardcoded.  Taking suggestions on a better way to do that.

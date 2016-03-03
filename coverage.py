#!/sw/bin/python3

""" short script to scrape TMXmoney.com for analyst coverage of all tickers """
# info is under http://web.tmxmoney.com/research.php?qm_symbol=XXX.UN (.UN is only for funds)
# steps will be
# DONE 1. create csv with two columns: ticker, coverage
# DONE 2. get list of all tsx listed stocks? (either download or, brute check tmx.. bad
# 3. scrape page for "there is no research information on file..." (can find in html)
""" CANNOT USE urllib python library, as it is not Javascript enabled """
# did that ever take a while to figure out...
# 4. handle for page not existing (in link address "invalid=true")
# 5. write csv
# 6. profit
""" long term"""
# 1. make list update from TMX website


import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time          # to not overdo it, we'll sleep a few seconds between page opens.
from bs4 import BeautifulSoup

TICKERS = []    # dictionary would be more mem efficient, but have use for list later
COVERAGE = {}
SITE = "http://web.tmxmoney.com/research.php?qm_symbol="

def make_csv(name):
    with open(name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ticker','coverage'])

def test_write(name):
    """simple test to make sure i'm appending correctly"""
    with open(name, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for i in range(10):
            writer.writerow([i, 'success'])

def make_tickers():
    """ read local csv of current listed companies (N=2259)"""
    global TICKERS
    with open('tsxListings_Mar2_2016.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            TICKERS.append(row[1]) # should read the ticker value
        if TICKERS[0] == str('ticker'):
            TICKERS.pop(0)
        assert (len(TICKERS) == 2259)

def parse_page(website):
    """ find analyst coverage in here for the input website"""
    # div.qm_maintext is the site's specific holder of analyst info.
    # specifically, if none, it contains <There is no research information on file for this symbol.>
    text = website.find("div", {"class": "qmResearch"})
    print(text)
    
def search_web():
    """ go through each ticker, and see if there is coverage. Use bs4 here.
         add to dictionary each item, and it's coverage status. Again, not most
         memory efficient, but is small enough to maintain list and dictionary."""
    for i in range(1): #len(TICKERS)) just 3 for test casing
        url = SITE + str(TICKERS[i])
        browser = webdriver.PhantomJS()
        try:
            browser.get(url)
            browser.find_element_by_id('qm_maintext')
        except TimeoutException as e:
            print(e)
        browser.quit()
        time.sleep(5)
        # OLD wayparse_page(soup)
        # now need to parse_page( "SAVED PAGE")

# see test_write for format
def write_csv():
    """ write dictionary key/value pairs to csv for use in excel """
    pass

def main():
    make_csv("tsxcoverage.csv")
    make_tickers()
#    test_write("tsxcoverage.csv")
    search_web()

if __name__ == "__main__":
    main()

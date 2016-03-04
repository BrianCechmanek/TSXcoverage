#!/sw/bin/python3

""" short script to scrape TMXmoney.com for analyst coverage of all tickers """
# info is under http://web.tmxmoney.com/research.php?qm_symbol=XXX.UN (.UN is only for funds)
# steps will be
# DONE 1. create csv with two columns: ticker, coverage
# DONE 2. get list of all tsx listed stocks? (either download or, brute check tmx.. bad
# DONE 3. scrape page for "there is no research information on file..." (can find in html)
""" CANNOT USE urllib python library, as it is not Javascript enabled """
# did that ever take a while to figure out...
# 4. handle for page not existing (in link address "invalid=true")
# DONE 5. write csv
# DONE 6. profit
""" long term"""
# 1. make list update from TMX website

import csv
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import random
import time          # to not overdo it, we'll sleep a few seconds between page opens.
import sys
# from bs4 import BeautifulSoup    # not currently used. will when raw HTML avail

TICKERS = []    # dictionary would be more mem efficient, but have use for list later
COVERAGE = {}
SITE = "http://web.tmxmoney.com/research.php?qm_symbol="

def make_csv(name):
    with open(name, 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ticker','coverage'])
        print("make_csv completed")
        
def write_csv(name):
    """ write dictionary key/value pairs to csv for use in excel """
    with open(name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['Final complete list', ' '])
        writer.writerow(['TICKER', 'COVERAGE'])
        for key, value in COVERAGE.items():
            writer.writerow([key, value])

def write_csv_row(name, count):
    """ write dictiaronary key/value to csv ROW in case of page shutout"""
    with open(name, 'a') as f:
        writer= csv.writer(f)
        writer.writerow([str(TICKERS[count]), COVERAGE[TICKERS[count]]])

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
    print("make_tickers completed")
    
def search_web():
    """ go through each ticker, and see if there is coverage. Use bs4 here.
         add to dictionary each item, and it's coverage status. Again, not most
         memory efficient, but is small enough to maintain list and dictionary."""
    print("searching the web...")
    for i in range(len(TICKERS)): #len(TICKERS)) just 3 for test casing
        url = SITE + str(TICKERS[i])
        print("\rSearching Ticker: %s      " %TICKERS[i], end=" ")
        browser = webdriver.PhantomJS()
        try:
            browser.get(url)
            element = browser.find_element_by_class_name('qm_maintext')
            if (element.get_attribute('innerHTML') == "There is no research information on file for this symbol."):
                COVERAGE[TICKERS[i]] = 0
            else:
                COVERAGE[TICKERS[i]] = 1
        except TimeoutException:
            print("TimeoutException after: " + str(i) + " sites accessed")
            print("skipped Ticker: " + TICKERS[i])
            time.sleep(300) # hopefully long enough for server
            continue
        write_csv_row('tsxcoverage.csv', i)    # just incasies
        #browser.quit()
        rand_time = random.randint(1,3)  # average 6 seconds between requests. should be fair
        time.sleep(rand_time)
        # OLD wayparse_page(soup)
        # now need to parse_page( "SAVED PAGE")
    browser.quit()
    print("\rsearch_web complete")

def main():
    make_csv("tsxcoverage.csv")
    make_tickers()
    search_web()
    if (len(COVERAGE) == 2259):
        write_csv("tsxcoverage.csv")
    print("done")
              
if __name__ == "__main__":
    main()

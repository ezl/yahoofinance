import httplib
import sys
import re
import simplejson as json
import threading
import time

from yfinance import YahooSymbol

"""
Live quotes from Yahoo Finance. Uses the same mechanism that Yahoo Finance web site uses
to update their quotes asynchronously on their pages.

Takes one argument, can accept multiple stock symbols separated by commas, no spaces.

Example:
    $ python delayed.py SPY,GOOG,YHOO,EBAY

"""

STREAMER_API = "streamerapi.finance.yahoo.com"
STREAMER_URL = ("/streamer/1.0"
                "?s=%s"
                "&k=%s"
                "&callback=parent.yfs_u1f"
                "&mktmcb=parent.yfs_mktmcb"
                "&gencallback=parent.yfs_gencb"
                )

def open(symbols="SPY,T,MSFT",data="l10,v00"):
    conn = httplib.HTTPConnection(STREAMER_API)
    url = STREAMER_URL % (symbols, data)
    conn.request("GET", url)
    return conn.getresponse()

def parse_line(line):
    if line.find('yfs_u1f') != -1:
        #return 'data: '+line
        #{"MSFT":{l10:"25.81",v00:"108,482,336"}}
        try:
            line = re.match(r".*?\((.*?)\)",line) # grab between the parentheses
            line = line.group(1)
            line = re.sub(r"(\w\d\d):",'"\\1":',line) # line isn't valid JSON
            return json.loads(line)
        except:
            return 'ERR: '+line
    elif line.find('yfs_mktmcb') != -1:
        line = re.match(r".*?\((.*?)\)",line) # grab between the parentheses
        line = line.group(1)
        return json.loads(line)
    else:
        return


def listen(symbols, pretty=True):
    conn = ''
    r = open(symbols,"l90") # l90 is the "last price" attribute

    line = ''

    while True:
        char = r.read(1)
        if char == '>':
            line += char
            data = parse_line(line)
            if data:
                if pretty:
                    try:
                        k, v = data.items()[0]
                        print "%s: %s" % (k, v['l90'])
                    except:
                        print(data)
                else:
                     print(data)
            line = ''
        else:
            line += char

    con.close();

if __name__ == "__main__":
    try:
        symbols = sys.argv[1]
    except:
        symbols = "SPY,GOOG,AAPL"

    try:
        listen(symbols)
    except:
        "Fail"


from yfinance import YahooFinance
import sys

"""
Grab a last price from Yahoo's delayed feed.

Takes one argument, can accept multiple stock symbols separated by commas, no spaces.

Example:
    $ python delayed.py SPY,GOOG,YHOO,EBAY
    SPY SPDR S&P 500 165.83
    GOOG Google Inc. 870.76
    YHOO Yahoo! Inc. 26.33
    EBAY eBay Inc. 55.10

"""


if __name__ == "__main__":
    yapi = YahooFinance()
    try:
        symbols = sys.argv[1]
    except:
        symbols = "GOOG,SPY"
    symbols = symbols.split(",")
    yapi.query_multiple(symbols)

    for symbol in symbols:
        s = yapi[symbol]
        print s.symbol, s.name, s.price

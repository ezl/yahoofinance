import re
import csv
import json
import time
import httplib
from urllib2 import urlopen, URLError


class YahooSymbol(object):
    """ Yahoo finance symbol """
    def __init__(self, symbol, name, price):
        self.symbol = symbol
        self.name = name
        self.price = price


class YahooFinance(dict):
    """ Yahoo finance API query """

    def query_multiple(self, symbols, data='l90'):
        """ Download and parse content """
        if not symbols:
            return
        symbols = [symbol.upper() for symbol in symbols]
        chunks_per = 200 # Can't request more than 200 symbols at once, so split into chunks
        for chunk in [symbols[i:i+chunks_per] for i in xrange(0, len(symbols), chunks_per)]:
            url = 'http://finance.yahoo.com/d/quotes.csv?s=%s&f=snl1' % '+'.join(chunk)
            while True:
                try:
                    reader = csv.reader(urlopen(url))
                    break
                except URLError:
                    pass # retry
            with open('/tmp/yfinance-csv.log', 'a', 1) as f:
                for line in reader:
                    symbol, name, price = line
                    f.write('%s %s %s %s\n' % (time.strftime("%Y-%m-%d %H:%M:%S"), price, symbol, name))
                    if price != '0.00' and float(price) < 100000.0:
                        self[symbol] = YahooSymbol(*line)

    def query_single(self, symbol):
        """ Shortcut method """
        self.query_multiple([symbol])
        return self[symbol]


    def __getitem__(self, name):
        """ Normalize symbol names """
        try:
            return dict.__getitem__(self, name.upper())
        except KeyError:
            return None

# available data items through the API
yahoo_items = {
    'a00': 'ask price',
    'b00': 'bid price',
    'g00': "day's range low",
    'h00': "day's range high",
    'j10': 'market cap',
    'v00': 'volume',
    'a50': 'ask size',
    'b60': 'bid size',
    'b30': 'ecn bid',
    'o50': 'ecn bid size',
    'z03': 'ecn ext hr bid',
    'z04': 'ecn ext hr bid size',
    'b20': 'ecn ask',
    'o40': 'ecn ask size',
    'z05': 'ecn ext hr ask',
    'z07': 'ecn ext hr ask size',
    'h01': "ecn day's high",
    'g01': "ecn day's low",
    'h02': "ecn ext hr day's high",
    'g11': "ecn ext hr day's low",
    't10': 'last trade time, will be in unix epoch format',
    't50': 'ecnQuote/last/time',
    't51': 'ecn ext hour time',
    't53': 'RTQuote/last/time',
    't54': 'RTExthourQuote/last/time',
    'l10': 'last trade',
    'l90': 'ecnQuote/last/value',
    'l91': 'ecn ext hour price',
    'l84': 'RTQuote/last/value',
    'l86': 'RTExthourQuote/last/value',
    'c10': 'quote/change/absolute',
    'c81': 'ecnQuote/afterHourChange/absolute',
    'c60': 'ecnQuote/change/absolute',
    'z02': 'ecn ext hour change',
    'z08': 'ecn ext hour change',
    'c63': 'RTQuote/change/absolute',
    'c85': 'RTExthourQuote/afterHourChange/absolute',
    'c64': 'RTExthourQuote/change/absolute',
    'p20': 'quote/change/percent',
    'c82': 'ecnQuote/afterHourChange/percent',
    'p40': 'ecnQuote/change/percent',
    'p41': 'ecn ext hour percent change',
    'z09': 'ecn ext hour percent change',
    'p43': 'RTQuote/change/percent',
    'c86': 'RTExtHourQuote/afterHourChange/percent',
    'p44': 'RTExtHourQuote/change/percent',
}

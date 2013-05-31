yahoofinance
============

Grab realtime and delayed quotes from yahoo finance

A utility I created a while back for a finance stock price notification app.

As far as I know, the actual streaming API that I'm using is not intended for public consumption nor is it actually documented anywhere.

At the time I created this, I just looked at how Yahoo was updating its pages then listened for the same mechanism.

It's a little messy, but it worked for me.

There are 2 files that get prices (realtime ticker and delayed):

## delayed.py ##

As the name suggests, it gets the last tick price of one or more symbols through the (documented) Yahoo Finance API, which can be up to 15 minutes delayed.  

Usage:

    $ python delayed.py SPY,GOOG,YHOO,EBAY
    SPY SPDR S&P 500 165.83
    GOOG Google Inc. 870.76
    YHOO Yahoo! Inc. 26.33
    EBAY eBay Inc. 55.10

## liveticker.py ##

This is the script that keeps listening for prices. It will output new prices to your console as it hears them. When testing on a box against my feed from Goldman Sachs, it was often within 500ms, and it wasn't uncommon for ticks to come in *before* Interactive Brokers.  It's been >2 years since I've looked though, so I can't vouch for the feed, though as of May 30 2013, it appears to still work.

Usage:

    $ python liveticker.py SPY,GOOG,YHOO,EBAY

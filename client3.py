import json
import random
import urllib.request

# Server API URLs
QUERY = "http://localhost:5000/query?id={}"

# 500 server requests
N = 500


def getDataPoint(quote):
    """ Produce all the needed values to generate a datapoint """
    if isinstance(quote, dict):
        stock = quote.get('stock', '')
        bid_price = float(quote.get('top_bid', {}).get('price', 0))
        ask_price = float(quote.get('top_ask', {}).get('price', 0))
        price = (bid_price + ask_price) / 2
        return stock, bid_price, ask_price, price
    else:
        print("Unexpected quote format:", quote)
        return None, None, None, None


def getRatio(price_a, price_b):
    """ Get ratio of price_a and price_b """
    if price_b == 0:
        return None
    return price_a / price_b


# Main
if __name__ == "__main__":
    # Query the price once every N seconds.
    for _ in range(N):
        try:
            # Make the API request
            response = urllib.request.urlopen(QUERY.format(random.random()))
            data = response.read()
            quotes = json.loads(data)

            # Print the raw response for inspection
            print("API Response:", quotes)

            prices = {}
            for quote in quotes:
                stock, bid_price, ask_price, price = getDataPoint(quote)
                if stock:
                    prices[stock] = price
                    print("Quoted %s at (bid:%s, ask:%s, price:%s)" % (stock, bid_price, ask_price, price))

            # Calculate and print the ratio if both stocks are present
            if "ABC" in prices and "DEF" in prices:
                ratio = getRatio(prices["ABC"], prices["DEF"])
                if ratio is not None:
                    print("Ratio %s" % ratio)
                else:
                    print("Error: Cannot calculate ratio. Division by zero.")
            else:
                print("Missing price data for one or both stocks.")

        except Exception as e:
            print("Error during request or processing:", e)

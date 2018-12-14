from auction import Input
from auction import Auction
import numpy as np


def round_average_market_prices(market_prices):
    round_averages = []
    for round_outcome in market_prices:
        round_averages.append(sum(round_outcome) / float(len(round_outcome)))
    return round_averages


def seller_average_market_prices(market_prices):
    seller_averages = []
    for seller_outcome in market_prices.T:
        seller_averages.append(sum(seller_outcome) / float(len(seller_outcome)))
    return seller_averages


def process_data(market_prices, buyer_profits, seller_profits):
    market_prices = np.reshape(market_prices, (auction_parameters.num_round, auction_parameters.num_seller))
    round_averages = round_average_market_prices(market_prices)
    seller_averages = seller_average_market_prices(market_prices)
    avg_buyer_profit_per_round = (sum(buyer_profits) / float(len(buyer_profits))) / auction_parameters.num_round
    avg_seller_profit_per_round = (sum(seller_profits) / float(len(seller_profits))) / auction_parameters.num_round
    avg_market_price = sum(map(sum, market_prices)) / (auction_parameters.num_seller * auction_parameters.num_round)
    return market_prices, round_averages, seller_averages, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price


auction_parameters = Input()
test = Auction(auction_parameters)
market_prices, buyer_profits, seller_profits = test.run()
market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = process_data(market_prices, buyer_profits, seller_profits)

print(f"Market Prices:")
for i, round_outcome in enumerate(market_prices):
    print(f"round {i}: {round_outcome}")
print()

print(f"Buyer profits for all {auction_parameters.num_round} rounds: \n{buyer_profits}\n"
      f"AVG Buyer profits per round: \n{avg_buyer_profit_per_round}\n"
      f"Seller profits for all {auction_parameters.num_round} rounds: \n{seller_profits}\n"
      f"AVG Seller profits per round: {avg_seller_profit_per_round}\n"
      f"AVG market price: {avg_market_price}\n")

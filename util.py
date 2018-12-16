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


def process_data(market_prices, auction_parameters, buyer_profits, seller_profits):
    market_prices = np.reshape(market_prices, (auction_parameters.num_round, auction_parameters.num_seller))
    round_averages = round_average_market_prices(market_prices)
    seller_averages = seller_average_market_prices(market_prices)
    avg_buyer_profit_per_round = (sum(buyer_profits) / float(len(buyer_profits))) / auction_parameters.num_round
    avg_seller_profit_per_round = (sum(seller_profits) / float(len(seller_profits))) / auction_parameters.num_round
    avg_market_price = sum(map(sum, market_prices)) / (auction_parameters.num_seller * auction_parameters.num_round)
    return market_prices, round_averages, seller_averages, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price
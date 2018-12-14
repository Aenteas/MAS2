from auction import Input
from auction import Auction
import numpy as np
import util

""" In this part we construct lists of legal parameter values for each variable parameter to the auction model """
min_number_sellers = 1
max_number_sellers = 10
num_sellers_param_list = list(range(min_number_sellers, max_number_sellers+1))

min_number_buyers = min_number_sellers + 1
max_number_buyers = (max_number_sellers + 1) * 2
num_buyers_param_list = list(range(min_number_buyers, max_number_buyers+1))

min_number_itemtype = 1
max_number_itemtype = max_number_sellers
num_itemtype_param_list = list(range(min_number_itemtype, max_number_itemtype+1))

min_number_rounds = 1
max_number_rounds = 20
num_rounds_param_list = list(range(min_number_rounds, max_number_rounds+1))

min_s_max = 1  # The s_max is the maximal starting price for auctions
max_s_max = 10
s_max_param_list = list(range(min_s_max, max_s_max+1))

min_fine = 0.1  # The part of the starting price used as a fine
max_fine = 1.2  # All of the starting price is used as a fine, in which case you get no money back for returning item
fine_param_list = np.arange(min_fine, max_fine, 0.1)
# End of parameter list generation

"""
FROM ASSIGNMENT TEXT:
Experiment with values of number of item types, number of sellers, number of buyers (Note: art with small values 
e.g. 1 and 2, and make little increments of e.g. 1), and number of rounds.

For each number of sellers defined in the parameter list above, run experiments with 1-10 more buyers than sellers,
and with a number of item types up to the amount of sellers.
"""
buyers_sellers_rounds_results = []  # This list will contain results of variations on buyers, sellers and rounds
for number_of_sellers in num_sellers_param_list:
    auction_parameters = Input()
    auction_parameters.num_seller = number_of_sellers
    for number_of_buyers in range(number_of_sellers+1, number_of_sellers + 10):
        auction_parameters.num_buyer = number_of_buyers
        for number_of_item_types in range(min_number_itemtype, number_of_sellers):
            auction_parameters.num_itemtype = number_of_item_types
            test = Auction(auction_parameters)
            market_prices, buyer_profits, seller_profits = test.run()
            market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
                market_prices, auction_parameters, buyer_profits, seller_profits)
            buyers_sellers_rounds_results.append([auction_parameters, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price])


"""
FROM ASSIGNMENT TEXT:
Experiment with values of penalty factor.
"""
auction_parameters = Input()
rounds_results = []  # This list will contain results of variations on amount of rounds in an auction
for number_of_rounds in num_rounds_param_list:
    auction_parameters.num_round = number_of_rounds
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    rounds_results.append([auction_parameters, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price])


"""
FROM ASSIGNMENT TEXT:
Experiment with values of bidding factors.
"""
auction_parameters = Input()
s_max_results = []  # This list will contain results of variations on maximal starting price
for s_max in s_max_param_list:
    auction_parameters.s_max = s_max
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    s_max_results.append([auction_parameters, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price])

"""
FROM
Experiment with values of bid in-/decrease factors.
"""
auction_parameters = Input()
fine_results = []  # This list will contain results of variations on annulation fees
for fine in fine_param_list:
    auction_parameters.fine = fine
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    fine_results.append([auction_parameters, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price])

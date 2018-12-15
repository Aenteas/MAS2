from auction import Input
from auction import Auction
import numpy as np
import util

""" In this part we construct lists of legal parameter values for each variable parameter to the auction model """
min_number_sellers = 1
max_number_sellers = 10
num_sellers_param_list = list(range(min_number_sellers, max_number_sellers+1))

min_number_itemtype = 1
max_number_itemtype = max_number_sellers
num_itemtype_param_list = list(range(min_number_itemtype, max_number_itemtype+1))

min_number_rounds = 1
max_number_rounds = 20
num_rounds_param_list = list(range(min_number_rounds, max_number_rounds+1))

bid_inc_factors = np.arange(1, 1.5, 0.1)
bid_dec_factors = np.arange(0.5, 1, 0.1)

bid_factor_param_list = list(range(1, 6))

min_fine = 0.1  # The amount of the starting price used as annulment fee
max_fine = 1.2
fine_param_list = np.arange(min_fine, max_fine, 0.1)
# End of parameter list generation

"""
FROM ASSIGNMENT TEXT:
Experiment with values of number of item types, number of sellers, number of buyers (Note: art with small values 
e.g. 1 and 2, and make little increments of e.g. 1), and number of item types.

For each number of sellers defined in the parameter list above, run experiments with 1-10 more buyers than sellers,
and with a number of item types up to the amount of sellers.
"""
results_buyers_sellers_items = []  # This list will contain results of variations on buyers, sellers and item types
for number_of_sellers in num_sellers_param_list:
    for number_of_buyers in range(number_of_sellers + 1, number_of_sellers + 10):
        for number_of_item_types in range(min_number_itemtype, number_of_sellers):
            auction_parameters = Input()
            auction_parameters.num_seller = number_of_sellers
            auction_parameters.num_buyer = number_of_buyers
            auction_parameters.num_itemtype = number_of_item_types
            test = Auction(auction_parameters)
            market_prices, buyer_profits, seller_profits = test.run()
            market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
                market_prices, auction_parameters, buyer_profits, seller_profits)
            results_buyers_sellers_items.append({"params":auction_parameters, "avg_buyer_profit_per_round":avg_buyer_profit_per_round, "avg_seller_profit_per_round":avg_seller_profit_per_round, "avg_market_price":avg_market_price, "market_prices":market_prices})


"""
FROM ASSIGNMENT TEXT:
Experiment with values of number of item types, number of sellers, number of buyers (Note: art with small values 
e.g. 1 and 2, and make little increments of e.g. 1), and number of item types.

This part varies number of item types
"""
results_rounds = []  # This list will contain results of variations on amount of rounds in an auction
for number_of_rounds in num_rounds_param_list:
    auction_parameters = Input()
    auction_parameters.num_round = number_of_rounds
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    results_rounds.append({"params":auction_parameters, "avg_buyer_profit_per_round":avg_buyer_profit_per_round, "avg_seller_profit_per_round":avg_seller_profit_per_round, "avg_market_price":avg_market_price, "market_prices":market_prices})


"""
FROM ASSIGNMENT TEXT:
Experiment with values of bid in-/decrease factors.
"""
results_bidding_inc_dec = []  # This list will contain results of variations on maximal starting price
for bid_inc_factor in bid_inc_factors:
    for bid_dec_factor in bid_dec_factors:
        auction_parameters = Input()
        auction_parameters.bid_inc = bid_inc_factor
        auction_parameters.bid_dec = bid_dec_factor
        test = Auction(auction_parameters)
        market_prices, buyer_profits, seller_profits = test.run()
        market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
            market_prices, auction_parameters, buyer_profits, seller_profits)
        results_bidding_inc_dec.append({"params":auction_parameters, "avg_buyer_profit_per_round":avg_buyer_profit_per_round, "avg_seller_profit_per_round":avg_seller_profit_per_round, "avg_market_price":avg_market_price, "market_prices":market_prices})


"""
FROM ASSIGNMENT TEXT:
Experiment with values of penalty factor.
"""
results_annulment_fee = []  # This list will contain results of variations on annulment fees
for fine in fine_param_list:
    auction_parameters = Input()
    auction_parameters.fine = fine
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    results_annulment_fee.append({"params":auction_parameters, "avg_buyer_profit_per_round":avg_buyer_profit_per_round, "avg_seller_profit_per_round":avg_seller_profit_per_round, "avg_market_price":avg_market_price, "market_prices":market_prices})


"""
FROM ASSIGNMENT TEXT:
Experiment with values of bidding factors.
"""
results_bidding_factor = []  # This list will contain results of variations on maximal bidding factor
for bid_factor in bid_factor_param_list:
    auction_parameters = Input()
    auction_parameters.max_bid = bid_factor
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    results_bidding_factor.append({"params":auction_parameters, "avg_buyer_profit_per_round":avg_buyer_profit_per_round, "avg_seller_profit_per_round":avg_seller_profit_per_round, "avg_market_price":avg_market_price, "market_prices":market_prices})

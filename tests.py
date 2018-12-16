from auction import Input
from auction import Auction
import numpy as np
import util
import pickle

""" In this part we construct lists of legal parameter values for each variable parameter to the auction model """
min_number_sellers = 1
max_number_sellers = 10
num_sellers_param_list = list(range(min_number_sellers, max_number_sellers+1))

max_number_buyers = max_number_sellers + 10

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

iterations_per_configuration = 100


def run_experiment(auction_parameters, iterations_per_configuration):
    tot_buyer_profit_per_round = 0
    tot_seller_profit_per_round = 0
    tot_avg_market_price = 0
    tot_market_prices = 0
    for _ in range(0, iterations_per_configuration):
        test = Auction(auction_parameters)
        market_prices, buyer_profits, seller_profits = test.run()
        market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
            market_prices, auction_parameters, buyer_profits, seller_profits)
        tot_buyer_profit_per_round += avg_buyer_profit_per_round
        tot_seller_profit_per_round += avg_seller_profit_per_round
        tot_avg_market_price += avg_market_price
        tot_market_prices += market_prices
    avg_buyer_profit_per_round = tot_buyer_profit_per_round / float(iterations_per_configuration)
    avg_seller_profit_per_round = tot_seller_profit_per_round / float(iterations_per_configuration)
    avg_market_price = tot_avg_market_price / float(iterations_per_configuration)
    market_prices = tot_market_prices / float(iterations_per_configuration)
    results = {"params": auction_parameters, "avg_buyer_profit_per_round": avg_buyer_profit_per_round,
         "avg_seller_profit_per_round": avg_seller_profit_per_round, "avg_market_price": avg_market_price,
         "market_prices": market_prices}
    return results


"""
FROM ASSIGNMENT TEXT:
Experiment with values of number of item types, number of sellers, number of buyers (Note: start with small values 
e.g. 1 and 2, and make little increments of e.g. 1), and number of item types.

For each number of sellers defined in the parameter list above, run experiments with 1-10 more buyers than sellers,
and with a number of item types up to the amount of sellers.
"""
results_buyers_sellers = []  # This list will contain results of variations on buyers, sellers and item type

avg_buyer_profits_per_round = np.zeros([num_sellers_param_list[-1]+10, num_sellers_param_list[-1]+2])
avg_seller_profits_per_round = np.zeros([num_sellers_param_list[-1]+10, num_sellers_param_list[-1]+2])
avg_market_prices = np.zeros([num_sellers_param_list[-1]+10, num_sellers_param_list[-1]+2])
buyer_sellers_result_matrices = {"avg_buyer_profits_per_round":avg_buyer_profits_per_round,"avg_seller_profits_per_round":avg_seller_profits_per_round, "avg_market_prices":avg_market_prices}
for number_of_sellers in num_sellers_param_list:
    for number_of_buyers in range(number_of_sellers + 1, max_number_buyers):
        auction_parameters = Input()
        auction_parameters.num_seller = number_of_sellers
        auction_parameters.num_buyer = number_of_buyers
        result = run_experiment(auction_parameters, iterations_per_configuration)
        results_buyers_sellers.append(result)
        avg_buyer_profits_per_round[auction_parameters.num_buyer][auction_parameters.num_seller] = result[
            "avg_buyer_profit_per_round"]
        avg_seller_profits_per_round[auction_parameters.num_buyer][auction_parameters.num_seller] = result[
            "avg_seller_profit_per_round"]
        avg_market_prices[auction_parameters.num_buyer][auction_parameters.num_seller] = result[
            "avg_market_price"]



results_item_types = []
for number_of_items in num_itemtype_param_list:
    auction_parameters = Input()
    auction_parameters.num_itemtype = number_of_items
    result = run_experiment(auction_parameters, iterations_per_configuration)
    results_item_types.append(result)



"""
FROM ASSIGNMENT TEXT:
Experiment with values of number of item types, number of sellers, number of buyers (Note: start with small values 
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
    results_rounds.append(run_experiment(auction_parameters, iterations_per_configuration))


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
        results_bidding_inc_dec.append(run_experiment(auction_parameters, iterations_per_configuration))

results_bidding_dec = []  # This list will contain results of variations on maximal starting price
for bid_dec_factor in bid_dec_factors:
    auction_parameters = Input()
    auction_parameters.bid_dec = bid_dec_factor
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    results_bidding_dec.append(run_experiment(auction_parameters, iterations_per_configuration))

results_bidding_inc = []  # This list will contain results of variations on maximal starting price
for bid_inc_factor in bid_inc_factors:
    auction_parameters = Input()
    auction_parameters.bid_inc = bid_inc_factor
    test = Auction(auction_parameters)
    market_prices, buyer_profits, seller_profits = test.run()
    market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(
        market_prices, auction_parameters, buyer_profits, seller_profits)
    results_bidding_inc.append(run_experiment(auction_parameters, iterations_per_configuration))


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
    results_annulment_fee.append(run_experiment(auction_parameters, iterations_per_configuration))


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
    results_bidding_factor.append(run_experiment(auction_parameters, iterations_per_configuration))

all_results = {"buyer_sellers_result_matrices":buyer_sellers_result_matrices, "results_buyers_sellers":results_buyers_sellers, "results_item_types":results_item_types, "results_rounds":results_rounds, "results_bidding_inc_dec":results_bidding_inc_dec, "results_bidding_inc":results_bidding_inc, "results_bidding_dec":results_bidding_dec, "results_annulment_fee":results_annulment_fee, "results_bidding_factor":results_bidding_factor}
pickling_on = open("results.pickle", "wb")
pickle.dump(all_results, pickling_on)
pickling_on.close()

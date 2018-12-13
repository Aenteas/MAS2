from auction import Input
from auction import Auction
import numpy as np

""" In this part we construct lists of legal parameter values for each variable parameter to the auction model """
min_number_buyers = 2
max_number_buyers = 21
num_buyers_param_list = list(range(min_number_buyers, max_number_buyers))

min_number_sellers = 1
max_number_sellers = 20
num_sellers_param_list = list(range(min_number_sellers, max_number_sellers))

min_number_itemtype = 1
max_number_itemtype = max_number_sellers
num_itemtype_param_list = list(range(min_number_itemtype, max_number_itemtype))

min_number_rounds = 1
max_number_rounds = 20
num_rounds_param_list = list(range(min_number_itemtype, max_number_itemtype))

min_s_max = 1  # The s_max is the maximal starting price for auctions
max_s_max = 10
s_max_param_list = list(range(min_number_itemtype, max_number_itemtype))

min_fine = 0.1  # The part of the starting price used as a fine
max_fine = 1  # All of the starting price is used as a fine, in which case you get no money back for returning the item
fine_param_list = np.arange(min_fine, max_fine, 0.1)
# End of parameter list generation

auction_parameters = Input()

test = Auction(auction_parameters)
market_prices, buyer_profits, seller_profits = test.run()

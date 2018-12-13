from auction import Input
from auction import Auction
import numpy as np

# here test code can be placed

auction_parameters = Input()

test = Auction(auction_parameters)
market_prices, buyer_profits, seller_profits = test.run()

market_prices = np.reshape(market_prices, (auction_parameters.num_round, auction_parameters.num_seller))
round_averages = []
seller_averages = []

for round_outcome in market_prices:
    round_averages.append(sum(round_outcome) / float(len(round_outcome)))

for seller_outcome in market_prices.T:
    seller_averages.append(sum(seller_outcome) / float(len(seller_outcome)))

np.reshape([0, 0, 1, 1, 2, 2, 3, 3], (2, 4))
# array([[0, 0, 1, 1],
#        [2, 2, 3, 3]])

print(f"Market Prices:")
for i, round_outcome in enumerate(market_prices):
    print(f"round {i}: {round_outcome}")
print()

print(f"Buyer profits: \n{buyer_profits}\n"
      f"AVG Buyer profits per round: \n{(sum(buyer_profits) / float(len(buyer_profits))) / auction_parameters.num_round}\n"
      f"Seller profits for all {auction_parameters.num_round} rounds: \n{seller_profits}\n"
      f"AVG Seller profits per round: {(sum(seller_profits) / float(len(seller_profits))) / auction_parameters.num_round}\n")

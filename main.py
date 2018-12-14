from auction import Input
from auction import Auction
import util


auction_parameters = Input()
test = Auction(auction_parameters)
market_prices, buyer_profits, seller_profits = test.run()
market_prices, round_avgs, seller_avgs, avg_buyer_profit_per_round, avg_seller_profit_per_round, avg_market_price = util.process_data(market_prices, auction_parameters, buyer_profits, seller_profits)

print(f"Market Prices:")
for i, round_outcome in enumerate(market_prices):
    print(f"round {i}: {round_outcome}")
print()

print(f"Buyer profits for all {auction_parameters.num_round} rounds: \n{buyer_profits}\n"
      f"AVG Buyer profits per round: \n{avg_buyer_profit_per_round}\n"
      f"Seller profits for all {auction_parameters.num_round} rounds: \n{seller_profits}\n"
      f"AVG Seller profits per round: {avg_seller_profit_per_round}\n"
      f"AVG market price: {avg_market_price}\n")

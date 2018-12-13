from auction import Input
from auction import Auction
# here test code can be placed


auction_parameters = Input()

test = Auction(auction_parameters)
market_prices, buyer_profits, seller_profits = test.run()

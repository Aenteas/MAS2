import numpy as np
import random
from random import shuffle

class Input:
    # default parameter setting
    num_itemtype = 10
    num_seller = 5
    num_buyer = 15
    num_round = 10
    s_max = 1
    fine = 0.1
    pure_commitment = True

    # parameters for the bidding strategy. We use the same for each buyer
    bid_start = 1
    bid_dec = 0.9
    bid_inc = 1.1
    # the chosen strategy
    use_default_strat = True

class Auction:

    def __init__(self, input):

        self.param = input

        self.rounds = []
        # order the auctions for each round
        for _ in range(self.param.num_round):
            x = [i for i in range(self.param.num_seller)]
            shuffle(x)
            self.rounds.append(x)

        self.selleritems = []
        #pick itemtype for each seller randomly
        for _ in range(self.param.num_seller):
            self.selleritems.append(random.randint(0,self.param.num_itemtype))

        #the list of market prices for each auction
        self.market_prices = []

        self.starting_prices = []
        #set the starting prize for each seller according to uniform(0,s_max)
        for _ in range(self.param.num_seller):
            self.starting_prices.append(random.uniform(0, self.param.s_max))

        #initialize array of bidding factors for each buyer with the same starting value
        # In case of the original strategy buyers have bidding factors for each seller.
        # Otherwise bidding factors are determined by the type of the item
        if self.param.use_default_strat:
            self.num_bid_factors = self.param.num_seller
        else:
            self.num_bid_factors = self.param.num_itemtype

        self.bid_factors = np.empty(shape=(self.param.num_buyer, self.num_bid_factors), dtype=float)
        self.bid_factors.fill(self.param.bid_start)

        self.seller_profits = np.zeros(shape=(self.param.num_seller,1), dtype=float)
        self.buyer_profits = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)

        #the bids of buyers are stored in every auction
        self.buyer_bids = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)

        # the amount added to the base price computed from the previous purchase (in the same round) is stored
        # here we store the additional bid that will be added to the base price
        if not self.param.pure_commitment:
            self.buyer_commitments = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)

            # we also store the winners' payments to subtract from the sellers' profit in case of annul
            self.buyer_payment = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)
            # and the seller whom the amount has been paid for each buyer
            self.paid_seller = np.empty(shape=(self.param.num_buyer, 1), dtype=int)
            # -1 means no payment yet
            self.paid_seller.fill(-1)

        #in pure commitment after a buyer purchased an item she/he wont participate in auctions until the end of the round
        #we use a list to maintain the remaining participants
        #in case of leveled commitment we do not remove any of the buyers from this list
        self.participants = [i for i in range(self.param.num_buyer)]

    #run the auctions
    def run(self):
        for auctions in self.rounds:
            for seller in auctions:
                self.take_bids(seller)
                self.add_market_price()
                winner = self.winner(seller)
                if self.param.use_default_strat:
                    self.original_bid_update(winner, seller)
                else:
                    self.improved_bid_update(winner, seller)
                self.update_profits(winner, seller)
                self.update_purchase_details(winner, seller)
                # remove the winner until the end of the round
                if self.param.pure_commitment:
                    self.participants.remove(winner)
            #initialize for the next round
            self.init_round()

        return (self.market_prices, self.buyer_profits, self.seller_profits)


    #compute the market price by averaging over bids in the current auction
    def add_market_price(self):
        result = 0.0

        #average over the buyers
        for buyer in self.participants:
            result += self.buyer_bids[buyer]
        result /= len(self.participants)
        self.market_prices.append(result)

    #determine the winner in seller's auction
    def winner(self, seller):
        #get the current market price
        market_price = self.market_prices[-1]

        # in case of we do not use the original strategy we have bid_factors per item type
        # choose the item belonging to the seller
        if not self.param.use_default_strat:
            seller = self.selleritems[seller]

        winner_bid = 0
        winner = 0

        for buyer in self.participants:
            buyer_bid = self.buyer_bids[buyer]
            # the winner is under the market price with the biggest bid
            # if there are more such buyers (with the same bid) we choose the first
            if winner_bid < buyer_bid and buyer_bid < market_price:
                winner_bid = buyer_bid
                winner = buyer

        return winner

    #determine the amount that the winner have to pay in seller's auction
    def payment(self, winner):
        payment_bid = 0

        #the bid that the winner took
        winner_bid = self.buyer_bids[winner]

        #we search for the biggest bid that is under the bid of winner
        for buyer in self.participants:
            buyer_bid = self.buyer_bids[buyer]
            if payment_bid < buyer_bid and buyer_bid < winner_bid:
                payment_bid = buyer_bid

        return payment_bid


    # increase the bid factor in case of lose otherwise decrease. This is the bidding strategy given in the specification
    def original_bid_update(self, winner, seller):
        for buyer in self.participants:
            #decrease if we won, increase if we lost
            if buyer == winner:
                self.bid_factors[buyer][seller] *= self.param.bid_dec
            else:
                self.bid_factors[buyer][seller] *= self.param.bid_inc

    # Here we decrease the bid factor if our bid was greater than or equal to the winners' bid. Otherwise we increase
    # Additionally the bid factors are determined by the item types rather than the sellers as in the original update
    def improved_bid_update(self, winner, seller):

        seller = self.selleritems[seller]

        # the bid that the winner took
        winner_bid = self.buyer_bids[winner]
        for buyer in self.participants:
            buyer_bid = self.buyer_bids[buyer]
            if buyer_bid >= winner_bid:
                self.bid_factors[buyer][seller] *= self.param.bid_dec
            else:
                self.bid_factors[buyer][seller] *= self.param.bid_inc

    # update the profits with the outcome of the current auction
    def update_profits(self, winner, seller):
        self.seller_profits[seller] += self.payment(self, winner, seller)

        self.buyer_profits[winner] += self.market_prices[-1] - self.seller_profits[seller]

        #if we use leveled commitment and buyer already has a purchase
        if not self.param.pure_commitment and self.paid_seller[winner] != -1:
            #pay the fine and get back the payment from the seller
            self.seller_profits[self.paid_seller[winner]] += self.fine * self.starting_prices[seller] - self.buyer_payment[winner]
            self.buyer_profits -= self.buyer_commitments[winner]


    #every buyer takes their own bid
    def take_bids(self, seller):
        #the starting price is always determined by the seller not the item type
        starting_price = self.starting_prices[seller]
        # in case of we do not use the original strategy we have bid_factors per item type
        # choose the item belonging to the seller
        if not self.param.use_default_strat:
            seller = self.selleritems[seller]

        #update each of
        for buyer in self.participants:
            self.buyer_bids[buyer] = self.bid_factors[buyer][seller] * starting_price

        # If we have leveled commitment we take into account the previous purchase
        if not self.param.pure_commitment:
            for buyer in self.participants:
                # take the maximum
                if self.buyer_commitments[buyer] + starting_price > self.buyer_bids[buyer]:
                    self.buyer_bids[buyer] = self.buyer_commitments[buyer] + starting_price

    # update the winners' commitment and payment for the next auctions in the current round
    def update_purchase_details(self, winner, seller):
        self.buyer_commitments[winner] = self.self.market_prices[-1] - self.payment(self, winner, seller) + \
                                         self.fine * self.starting_prices[seller]

        # update payment of buyer (amount and to whom)
        self.buyer_payment[winner] = self.payment(self, winner, seller)
        self.paid_seller[winner] = seller

    def init_round(self):
        if self.param.pure_commitment:
            self.participants = [i for i in range(self.param.num_buyer)]
        else:
            self.buyer_commitments = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)
            self.buyer_payment = np.zeros(shape=(self.param.num_buyer, 1), dtype=float)
            self.paid_seller = np.empty(shape=(self.param.num_buyer, 1), dtype=int)
            self.paid_seller.fill(-1)
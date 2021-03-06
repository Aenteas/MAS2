import numpy as np
import matplotlib.pyplot as plt
import pickle

# The file name of the opened file should be the same as the one pickled at the end of tests.py
pickling_on = open("results.pickle", "rb")
p = pickle.load(pickling_on)

fig1 = plt.figure()
plt.xlabel('Sellers', fontsize=18)
plt.ylabel('Buyers', fontsize=16)
plt.imshow(p["buyer_sellers_result_matrices"]["avg_buyer_profits_per_round"])
plt.show()

fig2 = plt.figure()
plt.xlabel('Sellers', fontsize=18)
plt.ylabel('Buyers', fontsize=16)
plt.imshow(p["buyer_sellers_result_matrices"]["avg_seller_profits_per_round"])
plt.show()

fig3 = plt.figure()
plt.xlabel('Sellers', fontsize=18)
plt.ylabel('Buyers', fontsize=16)
plt.imshow(p["buyer_sellers_result_matrices"]["avg_market_prices"])
plt.show()

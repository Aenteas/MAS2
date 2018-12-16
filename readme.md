# README

## auction.py
The core logic and default parameters of the auction simulation is located in the auction.py file.

## main.py
The main.py script runs a single simulation, with default parameters. It also acts as a simple case demo for how to run an auction with our model.

## Input and Auction classes
Parameters are controlled from the Input class, an can be edited there before initializing the Auction class. Inspect the Input class within auction.py to see the default parameters.

## tests.py
The tests.py script is used to run all experiments. Within it, you can see examples of how the Input class is manipulated to change parameters of the auction model. At the end of tests.py, the results are pickled (serialized with the pickle library). They are "unpickled" and used by the plot.py file.

## plot.py
The plot.py script was used to plot the 2d colour representations of the results of changing number of buyers and number of sellers simultaneously. It relies on reading serialized results from the tests.py file, stored directly in the project folder.

## util.py
The util.py file contains functions for processing the data outputted by the Auction model's .run() method, and transforming it into useful statistics.
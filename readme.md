# README

## auction.py
The core logic and default parameters of the auction simulation is located in the auction.py file.

## main.py
The main.py script runs a single simulation, with default parameters. It also acts as a simple case demo for how to run an auction with our model.

## Input and Auction classes
Parameters are controlled from the Input class, an can be edited there before initializing the Auction class. Inspect the Input class within auction.py to see the default parameters.
#### use_default_strat = true
You might notice that in the Input class there is a boolean parameter for whether to use the default strategy or not. 
If set to false, players will have the same bid factor for items of the same item type. 
It was an impulse about using the item type information for something, which we decided not to spend time deliberating or experimenting on in the report due to time constraints.

## tests.py
The tests.py script is used to run all experiments. Within it, you can see examples of how the Input class is manipulated to change parameters of the auction model. At the end of tests.py, the results are pickled (serialized with the pickle library). They are "unpickled" and used by the plot.py file.

## plot.py
The plot.py script was used to plot the 2d colour representations of the results of changing number of buyers and number of sellers simultaneously. It relies on reading serialized results from the tests.py file, stored directly in the project folder.

## util.py
The util.py file contains functions for processing the data outputted by the Auction model's .run() method, and transforming it into useful statistics.

## results.pickle
We attached a pickled results file for your convenience. It is not the same results that were used for the analysis in the report, but we included it nonetheless so that you can run the plot.py file without having to re-run tests.py yourself.

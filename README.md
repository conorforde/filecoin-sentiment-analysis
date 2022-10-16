# IPFS-integration-challenge


This project collects data about news events and the price of the Filecoin cryptocurrency every day. Currently I am trying to identify if there is a correlation between the sentiment of news headlines and the price of Filecoin cryptocurrency but I would like to extend this project to do the same for multiple cryptocurrencies.

To collect the news data I use the https://newsapi.org/ API to get news articles. Then to classify whether the headlines are positive or negative I am using nltk library from Python. I use the yFinance API to get the stock prices.

And all this data is being stored on the IPFS network and read the data from the IPFS network to identify trends in whether or not there is a correlation.

I am looking to expand this project to see if the results are similar across all cryptocurrencies, and the more data the better in this case.

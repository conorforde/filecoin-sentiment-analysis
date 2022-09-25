import requests
import nltk
import datetime as dt
import yfinance as yf
import subprocess
from nltk.sentiment.vader import SentimentIntensityAnalyzer
sent_analyzer = SentimentIntensityAnalyzer()

url = ('https://newsapi.org/v2/everything?'
       'q=Ethereum&'
       'from=2022-08-25&'
       'sortBy=popularity&'
       'apiKey=c2c65159bca849e0a1e18a2e0ff8893c')

response = requests.get(url)

symbol = 'ETH-USD'
ticker = yf.Ticker(symbol).info
start = dt.datetime(2020,1,1)
end = dt.datetime.now()

today = dt.date.today()

yesterday = today - dt.timedelta(days=1)

eth = yf.download('ETH-USD', yesterday, today)

eth_change=eth['Open'][1]-eth['Open'][0]
today = dt.datetime.now().strftime('%A')

pos_count=0
neg_count=0

total=len(response.json()['articles'])
file_name = 'test.txt'
f = open(file_name, 'w')

for i in range(len(response.json()['articles'])):
	
	sentence = response.json()['articles'][i]['title']
	sentiment = 'Neutral'
	compound = sent_analyzer.polarity_scores(sentence)['compound']
	if compound >= 0.05:
		sentiment = 'Positive'
		pos_count = pos_count + 1
	elif compound <= -0.05:
		sentiment = 'Negative'
		neg_count = neg_count + 1

pos_percent=(pos_count/total)
neg_percent=(neg_count/total)
nuetral_percent=100-(pos_percent+neg_percent)

file_data = symbol + ' => ' + 'pos: ' + str(pos_percent) + ' neg: ' + str(neg_percent) + '\n\n'

f.write(file_data)

f.close()

output = subprocess.check_output(["ipfs", "add", file_name])
output = output.decode('utf-8')
output = output.split(' ')[1]

f=open('hashes.txt', 'a')
f.write(str(today))
f.write(' : ')
f.write(str(output))
f.write('\n')
f.close()

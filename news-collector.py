import requests
import nltk
import datetime as dt
import yfinance as yf
import subprocess
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from scipy.stats import pearsonr
sent_analyzer = SentimentIntensityAnalyzer()

url = ('https://newsapi.org/v2/everything?'
       'q=Filecoin&'
       'from=2022-09-25&'
       'sortBy=popularity&'
       'apiKey=c2c65159bca849e0a1e18a2e0ff8893c')

response = requests.get(url)

symbol = 'FIL-USD'
ticker = yf.Ticker(symbol).info
start = dt.datetime(2020,1,1)
end = dt.datetime.now()

today = dt.date.today()

yesterday = today - dt.timedelta(days=1)

fil = yf.download('FIL-USD', yesterday, today)

fil_change=fil['Open'][1]-fil['Open'][0]
today = dt.datetime.now().strftime('%A')

file_change=round(float(fil_change),3)

pos_count=0
neg_count=0

total=len(response.json()['articles'])
file_name = 'test.txt'
f = open(file_name, 'a')

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

pos_percent=round(float(pos_percent),3)
neg_percent=round(float(neg_percent),3)

file_data = '\n' + str(dt.date.today())+ ' change: ' + str(fil_change) + ' ' + symbol + ' => ' + 'pos: ' + str(pos_percent) + ' neg: ' + str(neg_percent)

f.write(file_data)

f.close()
output = subprocess.check_output(["ipfs", "add", file_name])
output = output.decode('utf-8')
output = output.split(' ')[1]

f=open('hashes.txt', 'a')
f.write(str(dt.date.today()))
f.write(' : ')
f.write(str(output))
f.write('\n')
f.close()


f=open('test.txt', 'r')
lines = f.readlines()
change=[]
pos=[]
neg=[]

for line in lines:
    if len(line) == 1:
        break
    line = line.split(' ')
    #print(line)
    change.append(round(float(line[2]), 3))
    print('pos: ', round(float(line[-3]), 3))
    pos.append(round(float(line[-3]), 3))
    neg.append(round(float(line[-1]), 3))

#change = round(float(change), 3)
#neg = round(float(neg), 3)
#pos = round(float(pos), 3)

#print('change: ', change, pos, neg)
correlation_neg, p_value = pearsonr(change, pos)
correlation_pos, p_value = pearsonr(change, neg)

print('Negative news correlation: ', correlation_neg, 'Positive news correlation: ', correlation_pos)

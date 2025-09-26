import requests
import os
import time
import csv
from dotenv import load_dotenv
load_dotenv()

POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000
CALLS_PER_MIN = 5
SLEEP_SECONDS = 60 / CALLS_PER_MIN

URL = f"https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}"
response = requests.get(URL)
tickers = []

data = response.json()
for ticker in data['results']:
    tickers.append(ticker)



# print(data.keys())
while 'next_url' in data:
    print(f'requesting next page: {data["next_url"]}')
    time.sleep(SLEEP_SECONDS)
    response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
    data = response.json()
    print(data)
    for ticker in data['results']:
        tickers.append(ticker)
        
example_ticker = {'ticker': 'HTB',
     'name': 'HomeTrust Bancshares, Inc.',
     'market': 'stocks',
     'locale': 'us',
     'primary_exchange': 'XNYS',
     'type': 'CS',
     'active': True,
     'currency_name': 'usd',
     'cik': '0001538263',
     'composite_figi': 'BBG002CV5W70',
     'share_class_figi': 'BBG002CV5WZ9',
     'last_updated_utc': '2025-09-26T06:06:19.270134787Z'}
    
# Write CSV with schema based on example_ticker keys
fieldnames = list(example_ticker.keys())
with open('tickers.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
    writer.writeheader()
    for t in tickers:
        row = {k: t.get(k) for k in fieldnames}
        writer.writerow(row)
print(f"CSV written to tickers.csv with {len(tickers)} rows")

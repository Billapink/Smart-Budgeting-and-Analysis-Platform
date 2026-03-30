from faker import Faker
from datetime import date
import pandas as pd

fake = Faker()

merchants = ['ALIBABA.COM', 'PACKAGING SUPPLIES DIRECT', 'DHL EXPRESS', 'META ADS', 'GOOGLE ADS', 'TIKTOK ADS', 'SHELL', 'REGUS', 'BRITISH GAS', 'STRIPE PAYMENTS', 'SHOPIFY PAYOUT', 'MICROSOFT 365', 'ADOBE CREATIVE CLOUD', 'SLACK', 'ROYAL MAIL', 'STAPLES', 'HMRC PAYE', 'GUSTO', 'HMRC VAT', 'AMAZON', 'UBER', 'SALES']
descriptions = ['']

print('Date,Merchant,Amount')
rows = []
for i in range(1000):
    if i % 7 == 0:
        rows.append({
        "Date": fake.date_between(start_date=date(2020,1,1),end_date=date.today()),
        "Merchant": fake.random_element(merchants),
        "Amount": fake.random_int(1, 1000000000)/100,
        "Description": fake.random_element(descriptions)
    })

    rows.append({
        "Date": fake.date_between(start_date=date(2020,1,1),end_date=date.today()),
        "Merchant": fake.random_element(merchants),
        "Amount": fake.random_int(1, 10000000)/100,
        "Description": fake.random_element(descriptions)
    })

df = pd.DataFrame(rows)
df.to_csv("transactions.csv", index=False)
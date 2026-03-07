from faker import Faker
from datetime import date
import pandas as pd

fake = Faker()

merchants = ['ALIBABA.COM', 'PACKAGING SUPPLIES DIRECT', 'DHL EXPRESS', 'META ADS', 'GOOGLE ADS', 'TIKTOK ADS', 'SHELL', 'REGUS', 'BRITISH GAS', 'STRIPE PAYMENTS', 'SHOPIFY PAYOUT', 'MICROSOFT 365', 'ADOBE CREATIVE CLOUD', 'SLACK', 'ROYAL MAIL', 'STAPLES', 'HMRC PAYE', 'GUSTO', 'HMRC VAT', 'AMAZON', 'UBER']

print('Date,Merchant,Amount')
rows = []
for i in range(20):
    rows.append({
        "Date": fake.date_between(start_date=date(2025,1,1),end_date=date.today()),
        "Merchant": fake.random_element(merchants),
        "Amount": fake.random_int(1, 10000000)/100
    })

df = pd.DataFrame(rows)
df.to_csv("transactions.csv", index=False)
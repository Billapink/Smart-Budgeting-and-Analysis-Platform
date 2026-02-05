from faker import Faker

fake = Faker()

merchants = ['apple', 'banana', 'cherry', 'date', 'elderberry']

print('Merchant,Amount')
for i in range(20):
    merchant = fake.random_element(merchants)
    amount = fake.random_int(1, 100000)

    print(f'"{merchant}",{amount/100}')
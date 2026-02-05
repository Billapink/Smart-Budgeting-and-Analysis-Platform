import csv
import pandas as pd

class ImportAlgorithms:
    def __init__(self, transaction_repo):
        #passing in the transaction repository and defining required columns
        # for financial transaction data
        self.transaction_repo = transaction_repo
        self.required_columns = ["date", "merchant", "amount", "description"]

    def parse_csv(self, csv_file):
        transactions_dict = {}
        headers = []
        values=[]

        #reading the csv file 
        with open(csv_file, 'r') as csv:
            csv_reader= csv.reader(csv)

        #populating the headers array with the transaction data fields
        headers = next(csv_reader)
        #populating the transaction dictionary with the headers and an 
        # array of their corresponding values
        for header in headers:
            for row in csv_reader:
                values.append(row[header])
            transactions_dict.update({"%s": values} %header)
            values= []

        #parsing this dictionary into a dataframe for easier use
        df = pd.DataFrame(transactions_dict)

        #cast all types to their corresponding ones
        
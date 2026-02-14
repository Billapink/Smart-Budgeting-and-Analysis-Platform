import csv
import pandas as pd

class ImportAlgorithms:
    def __init__(self, transaction_repo):
        #passing in the transaction repository and defining required columns
        # for financial transaction data
        self.transaction_repo = transaction_repo
        self.required_columns = ["date", "merchant", "amount", "description"]

    def parse_csv(self, csv_file):
        transaction_rows = []

        #parsing the csv into a dataframe using pandas 
        df= pd.read_csv(csv_file)
        #assigning 'headers' to the column names of the dataframe
        headers= set(df.columns)
        #
        for element in headers:
            print(element)


        #cast all types to their corresponding ones
        
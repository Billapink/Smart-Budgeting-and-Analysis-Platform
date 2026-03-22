import csv
import pandas as pd

class ImportAlgorithms:
    def __init__ (self):
        # self.transaction_repo= getAuthorisationRepo()
        #passing in the transaction repository and defining required columns
        # for financial transaction data

        self.required_columns = ["date", "merchant", "amount"]

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
        
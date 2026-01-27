import csv
import pandas as pd
class ImportAlgorithms:
    def __init__(self, transaction_repo):
        self.transaction_repo = transaction_repo
        self.required_columns = ["date", "merchant", "amount", "description"]

    def parse_csv(self, csv_file):
        transactions_dict = {}
        headers = []
        values=[]
        with open(csv_file, 'r') as csv:
            csv_reader= csv.reader(csv)

        headers = next(csv_reader)


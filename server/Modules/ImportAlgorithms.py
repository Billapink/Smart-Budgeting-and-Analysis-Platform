from datetime import date

from Modules.CSVParser import parseCSV
from Modules.CategorisationAlgorithms import getCategorisationAlgorithms
from Repositories.BudgetAndTransactionRepository import getBugetAndTransactionRepo

class ImportAlgorithms:
    def __init__ (self):
        # self.transaction_repo= getAuthorisationRepo()
        #passing in the transaction repository and defining required columns
        # for financial transaction data

        self.required_columns = ["date", "merchant", "amount"]

    def import_csv(self, csv_string, companyID):
        try:
            csv = parseCSV(csv_string)
        except Exception as err:
            return ["error", f"Could not parse CSV: {err}"]

        # check that headers match required columns
        if len(csv["headers"]) != len(self.required_columns):
            return ["error", "CSV contains incorrect number of columns"]
        for (i, col) in enumerate(self.required_columns):
            if (col != csv["headers"][i].lower()):
                return ["error", "CSV contains incorrect columns"]
        
        # casting fields into the correct format and adding category
        categorisationAlgorithms = getCategorisationAlgorithms()
        categorisationAlgorithms.load_rules(companyID) # rules for the company need to be loaded
        transactions = csv["rows"]
        for tr in transactions:
            tr["companyID"] = companyID
            tr["date"] = date.fromisoformat(tr["date"])
            tr["amount"] = float(tr["amount"])
            tr["categoryID"] = categorisationAlgorithms.categorise_transaction(tr)
            tr["direction"] = "expense"

        bugetAndTransactionRepo = getBugetAndTransactionRepo()
        bugetAndTransactionRepo.insert_transactions(transactions)
        return ["success", "CSV transactions imported successfully"]
        
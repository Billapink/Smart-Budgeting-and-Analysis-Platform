from Modules.ImportAlgorithms import ImportAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository

dbCon = 'dummy'
repo = BudgetAndTransactionRepository(dbCon)
import_module = ImportAlgorithms(repo)
import_module.parse_csv('fake_data.csv')
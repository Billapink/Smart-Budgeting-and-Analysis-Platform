import datetime
from dateutil.relativedelta import relativedelta


class BudgetAndTransactionRepository:
    def __init__(self, dbCon):
        self.dbCon = dbCon
    
    def insert_transactions(self, transactions):
        data = []
        for t in transactions:
            data.append( (t["companyID"], t["date"].isoformat(), t["amount"], t["merchant"], t["categoryID"], t["direction"]) )
        
        self.dbCon.executemany(
            "INSERT INTO transactions(companyID, date, amount, merchant, categoryID, direction) VALUES (?,?,?,?,?,?)", 
            data)
    
    def update_transaction_category(self, transaction, categoryID):
        self.dbCon.execute(
            "UPDATE transactions SET categoryID = ? WHERE transactionID = ?", 
            (categoryID, transaction.transactionID))


    def monthly_totals(self, startDate):
        endDate = startDate + relativedelta(months = 1)
        res = self.dbCon.execute(
            "SELECT amount FROM transaction AS t WHERE t.date >= ? AND t.date < ?", 
            (startDate.isoformat(), endDate.isoformat()))
        
        sum = 0
        for row in res:
            sum += row[0]
        
        return sum


    def monthly_totals_by_category(self, startDate, categoryID):
        endDate = startDate + relativedelta(months = 1)
        res = self.dbCon.execute(
            "SELECT amount FROM transaction AS t WHERE t.date >= ? AND t.date < ? AND t.categoryID = ?", 
            (startDate.isoformat(), endDate.isoformat(), categoryID))
        
        sum = 0
        for row in res:
            sum += row[0]
        
        return sum
    
    def set_budget(self, budget):
        data = (budget["companyID"], budget["month"].isoformat(), budget["budget"], budget["categoryID"], budget["created_by"])
        self.dbCon.execute(
            "INSERT INTO budgets(companyID, month, budget, categoryID, created_by) VALUES (?, ?, ?, ?, ?)", 
            data)
    
    def get_budgets(self, month):
        endDate = month + relativedelta(months = 1)
        res = self.dbCon.execute(
            "SELECT budgetID, companyID, month, budget, categoryID, created_by FROM budgets AS b WHERE b.month >= ? AND b.month < ?", 
            (month.isoformat(), endDate.isoformat()))
        
        budgets = []
        for row in res:
            budgets.append({
                "budgetID": row[0],
                "companyID": row[1],
                "month": datetime.date.fromisoformat(row[2]),
                "budget": row[3],
                "categoryID": row[4],
                "created_by": row[5]
            })
        
        return budgets
    
    def update_budget(self, budget):
        data = (budget["companyID"], budget["month"].isoformat(), budget["budget"], budget["categoryID"], budget["created_by"], budget["budgetID"])
        self.dbCon.execute(
            "UPDATE budgets SET companyID = ?, month = ?, budget = ?, categoryID = ?, created_by = ? WHERE budgetID = ?", 
            data)

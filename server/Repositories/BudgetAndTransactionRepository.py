import datetime
from flask import g

from Data.database import getDB
from Modules.DateUtil import addMonth


class BudgetAndTransactionRepository:
    def __init__(self):
        self.dbCon = getDB()
    
    def insert_transactions(self, transactions):
        data = []
        for t in transactions:
            data.append( (t["companyID"], t["date"].isoformat(), t["amount"], t["merchant"], t["categoryID"], t["direction"]) )
        
        self.dbCon.executemany(
            "INSERT INTO transactions(companyID, date, amount, merchant, categoryID, direction) VALUES (?,?,?,?,?,?)", 
            data)
        self.dbCon.commit()
    
    def update_transaction_category(self, transaction, categoryID):
        self.dbCon.execute(
            "UPDATE transactions SET categoryID = ? WHERE transactionID = ?", 
            (categoryID, transaction.transactionID))
        self.dbCon.commit()


    def monthly_totals(self, startDate):
        endDate = addMonth(startDate)
        res = self.dbCon.execute(
            "SELECT amount FROM transactions AS t WHERE t.date >= ? AND t.date < ?", 
            (startDate.isoformat(), endDate.isoformat()))
        
        sum = 0
        for row in res:
            sum += row[0]
        
        return sum


    def monthly_totals_by_category(self, startDate, categoryID):
        endDate = addMonth(startDate)
        res = self.dbCon.execute(
            "SELECT amount FROM transactions WHERE date >= ? AND date < ? AND categoryID = ?", 
            (startDate.isoformat(), endDate.isoformat(), categoryID))
        
        sum = 0
        for row in res:
            sum += row[0]
        
        return sum
    
# budgetID INTEGER PRIMARY KEY, 
#         categoryID INTEGER,
#         created_by INTEGER, 
#         date, 
#         budget,

    def set_budget(self, startDate, categoryID, userID, budget):
        data = (startDate, categoryID, userID, budget)
        self.dbCon.execute(
            "INSERT INTO budgets(date, categoryID, created_by, budget) VALUES (?, ?, ?, ?)", 
            data)
        self.dbCon.commit()
    
    def get_budgets(self, month, categoryID):
        endDate = addMonth(month)
        res = self.dbCon.execute(
            "SELECT budgetID, created_by, date, budget FROM budgets AS b WHERE b.date >= ? AND b.date < ? AND categoryID = ?", 
            (month.isoformat(), endDate.isoformat(),categoryID)
        ).fetchall()
        
        budgets = []
        for row in res:
            budgets.append({
                "budgetID": int(row[0]),
                "created_by": row[1],
                "date": datetime.date.fromisoformat(row[2]),
                "budget": float(row[3]),
                "categoryID": categoryID
            })
        
        return budgets

    def get_budget_id(self, month, categoryID):
        endDate = addMonth(month)
        res = self.dbCon.execute(
            "SELECT budgetID FROM budgets AS b WHERE b.date >= ? AND b.date < ? AND categoryID = ?", 
            (month.isoformat(), endDate.isoformat(),categoryID)
        ).fetchall()
        if len(res) > 0:
            return res[0][0]

    def update_budget(self, startDate, categoryID, userID, budget, budgetID):
        data = (startDate, budget, categoryID, userID, budgetID)
        self.dbCon.execute(
            "UPDATE budgets SET date = ?, budget = ?, categoryID = ?, created_by = ? WHERE budgetID = ?", 
            data)
        self.dbCon.commit()


def getBugetAndTransactionRepo():
    if "transaction_repo" in g:
        return g.transaction_repo;

    g.transaction_repo = BudgetAndTransactionRepository()
    return g.transaction_repo
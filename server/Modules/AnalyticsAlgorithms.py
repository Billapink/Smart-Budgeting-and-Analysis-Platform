from dateutil.relativedelta import relativedelta
from flask import g

from Repositories.BudgetAndTransactionRepository import getBugetAndTransactionRepo
from Repositories.CategorisationRepository import getCategorisationRepo
from Modules.DateUtil import addMonth, firstOfMonth, lastOfMonth
from Modules.MergeSort import merge_sort

class AnalyticsAlgorithms:
    def __init__(self):
        self.transaction_repo = getBugetAndTransactionRepo()
        self.categories_repo = getCategorisationRepo()
    
    def get_monthly_totals_by_category_name(self, startOfMonth, companyID, categoryName):
        categoryID = self.categories_repo.get_category_id_by_name(companyID, categoryName)
        print("TRANS", categoryName, categoryID)
        return self.transaction_repo.monthly_totals_by_category(startOfMonth, categoryID)

    def compute_kpis(self, startOfMonth, companyID):
        revenue = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "Revenue")
        COGS = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "COGS")
        OpExp = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "OpExp")
        Taxes = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "Tax")
        Payroll = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "Payroll")
        SaaS = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "SaaS")
        Marketing = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "Marketing")
        Admin = self.get_monthly_totals_by_category_name(startOfMonth, companyID, "Admin")

        OpExpTotal = OpExp + Payroll + SaaS + Marketing + Admin
        if revenue == 0:
            revenue = 0.01

        KPIS = {
            "Revenue": revenue,
            "GrossProfit": revenue - COGS,
            "GrossProfitMargin": 100*(revenue - COGS)/revenue,
            "NetProfit": revenue - COGS - OpExpTotal - Taxes,
            "NetProfitMargin": 100*(revenue - COGS - OpExpTotal - Taxes)/revenue,
            "COGS": COGS
        }
        
        return KPIS

    def compute_trends(self, startDate, endDate, kpiChoice, companyID):
        '''
        Calculates the difference between the average kpi between a month and the previous month
        '''
        startMonth = firstOfMonth(startDate)
        endMonth = lastOfMonth(endDate)

        kpiValues = []
        currentMonth = startMonth
        while currentMonth < endMonth:
            KPIs = self.compute_kpis(currentMonth, companyID)
            kpiValues.append({
                "kpi": KPIs[kpiChoice],
                "month": currentMonth.isoformat()
            })
            currentMonth = addMonth(currentMonth)

        return kpiValues

    def compute_variances(self, startDate, endDate, categoryID):
        '''
        Calculates the difference between the average kpi between a month and the previous month
        '''
        startMonth = firstOfMonth(startDate)
        endMonth = lastOfMonth(endDate)

        variances = []
        currentMonth = startMonth
        while currentMonth < endMonth:
            actual = self.transaction_repo.monthly_totals_by_category(currentMonth, categoryID)
            budget = self.transaction_repo.get_budgets(currentMonth, categoryID)
            budgetValue = budget[0]["budget"] if len(budget) > 0 else 0.0
            variances.append({
                "variance": actual - budgetValue,
                "month": currentMonth.isoformat()
            })
            currentMonth = addMonth(currentMonth)

        return variances
    
    def compute_forecast(self, startDate, endDate, categoryID):
        '''
        Calculates the difference between the average kpi between a month and the previous month
        '''
        startMonth = firstOfMonth(startDate)
        endMonth = lastOfMonth(endDate)

        monthly_totals = []
        currentMonth = startMonth
        while currentMonth < endMonth:
            total = self.transaction_repo.monthly_totals_by_category(currentMonth, categoryID)
            monthly_totals.append(total)
            currentMonth = addMonth(currentMonth)

        if len(monthly_totals) < 3:
            raise RuntimeError("Require at least 3 months to make a forecast")

        sum = 0        
        for (i, total) in enumerate(monthly_totals):
            if i < len(monthly_totals) - 3:
                sum += total
            else:
                sum += 1.3*total

        return sum / (len(monthly_totals) + 0.9)
    
    def get_median(self, data):
        sorted = merge_sort(data)
        middle = len(sorted) // 2
        return sorted[middle]
    
    def compute_anomalies(self, startDate, endDate, categoryID):
        startMonth = firstOfMonth(startDate)
        endMonth = lastOfMonth(endDate)

        monthly_totals = []
        months = []
        currentMonth = startMonth
        while currentMonth < endMonth:
            total = self.transaction_repo.monthly_totals_by_category(currentMonth, categoryID)
            monthly_totals.append(total)
            months.append(currentMonth)
            currentMonth = addMonth(currentMonth)
        
        median = self.get_median(monthly_totals)
        deviations = [abs(median - tot) for tot in monthly_totals]
        MAD = self.get_median(deviations)

        outliers = []
        for (i, dev) in enumerate(deviations):
            score = 0.6745 * dev / MAD
            if score >= 3.5:
                outliers.append({
                    "month": months[i],
                    "total": monthly_totals[i],
                    "deviation": dev,
                    "score": score
                })
        
        return outliers
    
    def set_budget(self, startDate, categoryID, userID, budget):
        budgetID = self.transaction_repo.get_budget_id(startDate, categoryID)
        if budgetID == None:
            self.transaction_repo.set_budget(startDate, categoryID, userID, budget)
        else:
            print(f"Updating budget {budgetID} to {budget}")
            self.transaction_repo.update_budget(startDate, categoryID, userID, budget, budgetID)

def getAnalyticsAlgorithms():
    if "analytics_algorithms" in g:
        return g.analytics_algorithms;

    g.analytics_algorithms = AnalyticsAlgorithms()
    return g.analytics_algorithms
from dateutil.relativedelta import relativedelta
from flask import g

from Repositories.BudgetAndTransactionRepository import getBugetAndTransactionRepo
from Repositories.CategorisationRepository import getCategorisationRepo

class AnalyticsAlgorithms:
    def __init__(self):
        self.transaction_repo = getBugetAndTransactionRepo()
        self.categories_repo = getCategorisationRepo()
        # self.KPI_list = KPI_list
        # self.forecase_window = forecase_window
        # self.moving_avg_weights = moving_avg_weights
    
    def get_monthly_totals_by_category_name(self, startOfMonth, companyID, categoryName):
        categoryID = self.categories_repo.get_category_id_by_name(companyID, categoryName)
        print("TRANS", categoryName, categoryID)
        return self.transaction_repo.monthly_totals_by_category(startOfMonth, categoryID)

    def aggregate_monthly(self):
        pass

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

        KPIS = {
            "Revenue": revenue,
            "GrossProfit": revenue - COGS,
            "GrossProfitMargin": 100*(revenue - COGS)/revenue,
            "NetProfit": revenue - COGS - OpExpTotal - Taxes,
            "NetProfitMargin": 100*(revenue - COGS - OpExpTotal - Taxes)/revenue,
            "COGS": COGS
        }
        
        return KPIS

    def compute_mom(self, month, kpi):
        '''
        Calculates the difference between the average kpi between a month and the previous month
        '''


        previousMonth = month + relativedelta(months = -1)
        # kpis = self.compute_kpis(month)
        # kpisPrevious = self.compute_kpis(previousMonth)


        # return kpis[kpi] - kpisPrevious[kpi]

def getAnalyticsAlgorithms():
    if "analytics_algorithms" in g:
        return g.analytics_algorithms;

    g.analytics_algorithms = AnalyticsAlgorithms()
    return g.analytics_algorithms
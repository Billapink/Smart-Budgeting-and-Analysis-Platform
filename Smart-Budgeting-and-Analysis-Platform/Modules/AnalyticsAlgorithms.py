from dateutil.relativedelta import relativedelta

class AnalyticsAlgorithms:
    def __init__(self, transaction_repo, KPI_list, forecase_window, moving_avg_weights):
        self.transaction_repo = transaction_repo
        self.KPI_list = KPI_list
        self.forecase_window = forecase_window
        self.moving_avg_weights = moving_avg_weights
    
    def aggregate_monthly(self):
        pass


    def compute_kpis(self, month):
        revenue = self.transaction_repo.monthly_totals_by_category(month, "Revenue")
        COGS = self.transaction_repo.monthly_totals_by_category(month, "COGS")
        OpExp = self.transaction_repo.monthly_totals_by_category(month, "OpExp")
        Taxes = self.transaction_repo.monthly_totals_by_category(month, "Tax")


        KPIS = {
            "Revenue": revenue,
            "GrossProfit": revenue - COGS,
            "GrossProfitMargin": 100*(revenue - COGS)/revenue,
            "NetProfit": revenue - COGS - OpExp - Taxes,
            "NetProfitMargin": 100*(revenue - COGS - OpExp - Taxes)/revenue,
            "COGS": COGS
        }
        
        return KPIS


    def compute_mom(self, month, kpi):
        '''
        Calculates the difference between the average kpi between a month and the previous month
        '''

        previousMonth = month + relativedelta(months = -1)
        kpis = self.compute_kpis(month)
        kpisPrevious = self.compute_kpis(previousMonth)

        return kpis[kpi] - kpisPrevious[kpi]
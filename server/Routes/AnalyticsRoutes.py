from flask import Blueprint, request

from Modules.AnalyticsAlgorithms import AnalyticsAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository

repo = BudgetAndTransactionRepository([])
analytics = AnalyticsAlgorithms(repo, [], [],[])

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/get_kpis", methods=["GET"])
def get_kpis():
    month = request.args["month"]
    kpis = analytics.compute_kpis(month)
    return kpis

@analytics_bp.route("/get_trends", methods=["GET"])
def get_trends():
    # do something
    return []

@analytics_bp.route("/get_variance", methods=["GET"])
def get_variance():
    # do something
    return []

@analytics_bp.route("/get_forecast", methods=["GET"])
def get_forecast():
    # do something
    return []

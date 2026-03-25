from datetime import date

from flask import Blueprint, jsonify, request

from Modules.AnalyticsAlgorithms import getAnalyticsAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/get_kpis", methods=["GET"])
def get_kpis():
    print('GET KPIs')
    startDate = date.fromisoformat(request.args["date"])
    companyID = request.args["companyID"]
    analytics = getAnalyticsAlgorithms()
    kpis = analytics.compute_kpis(startDate, companyID)
    resp = jsonify(kpis)
    print('KPIS', kpis, resp)
    resp.status_code = 200

    return resp

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

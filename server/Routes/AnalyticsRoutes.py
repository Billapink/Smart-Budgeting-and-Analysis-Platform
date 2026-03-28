from datetime import date
import traceback

from flask import Blueprint, jsonify, request

from Modules.AnalyticsAlgorithms import getAnalyticsAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository
from Modules.DateUtil import firstOfMonth

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route("/get_kpis", methods=["GET"])
def get_kpis():
    try:
        startDate = date.fromisoformat(request.args["date"])
        companyID = request.args["companyID"]
        analytics = getAnalyticsAlgorithms()
        kpis = analytics.compute_kpis(startDate, companyID)
        resp = jsonify(kpis)
        resp.status_code = 200
    except Exception as err:
        return f"Error: {err=}", 400

    return resp

@analytics_bp.route("/get_trends", methods=["GET"])
def get_trends():
    try:
        startDate = date.fromisoformat(request.args["start_date"])
        endDate = date.fromisoformat(request.args["end_date"])
        kpi = request.args["kpi"]
        companyID = request.args["companyID"]
        analytics = getAnalyticsAlgorithms()
        kpis = analytics.compute_trends(startDate, endDate, kpi, companyID)
        resp = jsonify(kpis)
        resp.status_code = 200
    except Exception as err:
        return f"Error: {err=}", 400

    return resp

@analytics_bp.route("/get_variance", methods=["GET"])
def get_variance():
    try:
        startDate = firstOfMonth(date.fromisoformat(request.args["start_date"]))
        endDate = firstOfMonth(date.fromisoformat(request.args["end_date"]))
        categoryID = request.args["categoryID"]
        analytics = getAnalyticsAlgorithms()
        variances = analytics.compute_variances(startDate, endDate, categoryID)
        resp = jsonify(variances)
        resp.status_code = 200
    except Exception as err:
        print(err)
        print(traceback.format_exc())
        return f"Error: {err=}", 400
    
    return resp

@analytics_bp.route("/get_forecast", methods=["GET"])
def get_forecast():
    try:
        startDate = firstOfMonth(date.fromisoformat(request.args["start_date"]))
        endDate = firstOfMonth(date.fromisoformat(request.args["end_date"]))
        categoryID = request.args["categoryID"]
        analytics = getAnalyticsAlgorithms()
        forecast = analytics.compute_forecast(startDate, endDate, categoryID)
    except Exception as err:
        print(err)
        print(traceback.format_exc())
        return f"Error: {err=}", 400
    
    return str(forecast), 200
    
    return resp


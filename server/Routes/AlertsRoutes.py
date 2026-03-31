from datetime import date
import traceback

from flask import Blueprint, jsonify, request

from Modules.AnalyticsAlgorithms import getAnalyticsAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository
from Modules.DateUtil import firstOfMonth

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route("/get_anomalies", methods=["GET"])
def get_anomalies():
    try:
        startDate = firstOfMonth(date.fromisoformat(request.args["start_date"]))
        endDate = firstOfMonth(date.fromisoformat(request.args["end_date"]))
        categoryID = request.args["categoryID"]
        analytics = getAnalyticsAlgorithms()
        anomalies = analytics.compute_anomalies(startDate, endDate, categoryID)
        resp = jsonify(anomalies)
        resp.status_code = 200
        return resp
    except Exception as err:
        print(err)
        print(traceback.format_exc())
        return f"Error: {err=}", 400

@alerts_bp.route("/post_anomalies", methods=["POST"])
def post_anomalies():
    # do something here
    return ""

@alerts_bp.route("/patch_anomalies", methods=["POST"])
def patch_anomalies():
    # do something here
    return []
from flask import Blueprint

alerts_bp = Blueprint('alerts', __name__)


@alerts_bp.route("/get_anomalies", methods=["GET"])
def get_anomalies():
    # do something here
    return []

@alerts_bp.route("/post_anomalies", methods=["POST"])
def post_anomalies():
    # do something here
    return ""

@alerts_bp.route("/patch_anomalies", methods=["POST"])
def patch_anomalies():
    # do something here
    return []
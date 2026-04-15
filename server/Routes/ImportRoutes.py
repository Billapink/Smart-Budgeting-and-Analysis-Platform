import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from Modules.ImportAlgorithms import ImportAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository

import_alg = ImportAlgorithms()

import_routes_bp = Blueprint('import', __name__)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@import_routes_bp.route("/import_csv", methods=["POST"])
def import_csv():
    try:
        message = request.get_json()
        csvString = message["csv"]
        companyID = message["companyID"]

        import_alg.import_csv(csvString, companyID)
        return "", 200
    
    except Exception as err:
        return f"ERROR: {err} ", 400

    
@import_routes_bp.route("/import_status", methods=["POST"])
def import_status():
    # do something here
    return ""
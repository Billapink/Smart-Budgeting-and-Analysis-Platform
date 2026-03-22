from flask import Blueprint, request, make_response

from Modules.AuthorisationAlgorithms import getAuthorisationAlgorithms
from Modules.CategorisationAlgorithms import getCategorisationAlgorithms

admin_bp = Blueprint('admin', __name__)

@admin_bp.route("/create_company", methods=["POST"])
def createCompany():
    data = request.get_json()
    userID = data["userID"]
    company = data["company"]
    authorisation = getAuthorisationAlgorithms()
    [status, data] = authorisation.create_company(userID, company)
    if status == "success":
        return str(data), 200
    
    return data, 403;

@admin_bp.route("/create_category", methods=["POST"])
def createCategory():
    message = request.get_json()
    companyID = message["companyID"]
    category = message["category"]
    categoryType = message["type"]
    categorisation = getCategorisationAlgorithms()
    [status, message] = categorisation.create_category(companyID, category, categoryType)
    
    return message, 200 if status == "success" else 403;



@admin_bp.route("/create_rule", methods=["POST"])
def createRule():
    message = request.get_json()
    companyID = message["companyID"]
    categoryID = message["categoryID"]
    matchType = message["matchType"]
    pattern = message["pattern"]
    priority = message["priority"]
    categorisation = getCategorisationAlgorithms()
    [status, message] = categorisation.create_rule(companyID, categoryID, matchType, pattern, priority)
    
    return message, 200 if status == "success" else 403;

@admin_bp.route("/get_categories", methods=["GET"])
def getCategories():
    companyID    = int(request.args.get("companyID")) # type: ignore
    categorisation = getCategorisationAlgorithms()
    [status, data] = categorisation.get_categories(companyID)

    code = 200 if status == "success" else 403
    return data, code;

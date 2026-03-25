from flask import Blueprint, request, make_response

from Modules.AuthorisationAlgorithms import getAuthorisationAlgorithms
from Modules.CategorisationAlgorithms import getCategorisationAlgorithms
from Modules.AnalyticsAlgorithms import getAnalyticsAlgorithms

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
    
    return data, 400;

@admin_bp.route("/create_category", methods=["POST"])
def createCategory():
    message = request.get_json()
    companyID = message["companyID"]
    category = message["category"]
    categoryType = message["type"]
    categorisation = getCategorisationAlgorithms()
    [status, message] = categorisation.create_category(companyID, category, categoryType)
    
    return message, 200 if status == "success" else 400;


@admin_bp.route("/get_categories", methods=["GET"])
def getCategories():
    try:
        companyID    = int(request.args.get("companyID")) # type: ignore
        categorisation = getCategorisationAlgorithms()
        data = categorisation.get_categories(companyID)
    except Exception as err:
        return f"Error: {err=}", 400

    return data, 200


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
    
    return message, 200 if status == "success" else 400;


@admin_bp.route("/get_rules", methods=["GET"])
def getRules():
    print('CHECK A')
    try:
        companyID    = int(request.args.get("companyID")) # type: ignore
        categorisation = getCategorisationAlgorithms()
        data = categorisation.get_rules(companyID)
    except Exception as err:
        return f"Error: {err=}", 400
    print(data)
    return data, 200


@admin_bp.route("/set_rule_active", methods=["POST"])
def setRuleActive():
    try:
        message = request.get_json()
        ruleID = message["ruleID"]
        active = message["active"]        
        categorisation = getCategorisationAlgorithms()
        categorisation.set_rule_active(ruleID, active)
    except Exception as err:
        return f"Error: {err=}", 400
    
    return "success", 200

@admin_bp.route("/update_rule_priority", methods=["POST"])
def updateRulePriority():
    try:
        message = request.get_json()
        ruleID = message["ruleID"]
        priority = message["priority"]        
        categorisation = getCategorisationAlgorithms()
        categorisation.update_rule_priority(ruleID, priority)
    except Exception as err:
        return f"Error: {err=}", 400
    
    return "success", 200

@admin_bp.route("/set_budget", methods=["POST"])
def get_trends():
    try:
        startDate = date.fromisoformat(request.args["date"])
        categoryID = request.args["categoryID"]
        userID = request.args["userID"]
        budget = request.args["budget"]
        analytics = getAnalyticsAlgorithms()
        analytics.set_budget(startDate, categoryID, userID, budget)
    except Exception as err:
        return f"Error: {err=}", 400

    return "success", 200
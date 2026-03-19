from flask import Blueprint, request, make_response

from Modules.AuthorisationAlgorithms import getAuthorisationAlgorithms

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


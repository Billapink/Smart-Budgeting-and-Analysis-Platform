from flask import Blueprint, request, make_response

from Modules.AuthorisationAlgorithms import getAuthorisationAlgorithms

authorisation_bp = Blueprint('authorisation', __name__)

@authorisation_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    authorisation = getAuthorisationAlgorithms()
    [status, message] = authorisation.login(username, password)
    code = 400 if status == "success" else 403
    return message, code;

@authorisation_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    authorisation = getAuthorisationAlgorithms()
    [status, message] = authorisation.register_user(username, password)
    print('/register', status, message)
    code = 200 if status == "success" else 403
    return message, code;

@authorisation_bp.route("/join_company", methods=["POST"])
def join_company():
    data = request.get_json()
    user_id    = data["user_id"]
    company_id = data["company_id"]
    role       = data["role"]
    code_input = data["code_input"]
    authorisation = getAuthorisationAlgorithms()
    [status, message] = authorisation.join_company_by_code(user_id, company_id, role, code_input)
    return "success"

@authorisation_bp.route("/logout", methods=["POST"])
def logout():
    return "success"


from flask import Blueprint, request, make_response

from Modules.AuthorisationAlgorithms import getAuthorisationAlgorithms

authorisation_bp = Blueprint('authorisation', __name__)

@authorisation_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        authorisation = getAuthorisationAlgorithms()
        return str(authorisation.login(username, password)), 200
    except Exception as err:
        return f"Error: {err=}", 400
    

@authorisation_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        authorisation = getAuthorisationAlgorithms()
        authorisation.register_user(username, password)
    except Exception as err:
        return f"Error: {err=}", 400

@authorisation_bp.route("/get_memberships", methods=["GET"])
def get_memberships():
    user_id    = int(request.args.get("user_id")) # type: ignore
    authorisation = getAuthorisationAlgorithms()
    [status, data] = authorisation.get_memberships(user_id)
    code = 200 if status == "success" else 403
    return data, code;

@authorisation_bp.route("/join_company", methods=["POST"])
def join_company():
    data = request.get_json()
    user_id    = int(data["user_id"])
    company_id = int(data["company_id"])
    role       = data["role"]
    code_input = int(data["code_input"])
    authorisation = getAuthorisationAlgorithms()
    [status, message] = authorisation.join_company_by_code(user_id, company_id, role, code_input)
    code = 200 if status == "success" else 403
    return message, code;

@authorisation_bp.route("/logout", methods=["POST"])
def logout():
    return "success"


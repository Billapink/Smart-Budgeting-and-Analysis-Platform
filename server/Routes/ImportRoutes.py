import os
from flask import Blueprint, request, current_app
from werkzeug.utils import secure_filename

from Modules.ImportAlgorithms import ImportAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository

repo = BudgetAndTransactionRepository([])
import_alg = ImportAlgorithms(repo)

import_routes_bp = Blueprint('alerts', __name__)

ALLOWED_EXTENSIONS = {'csv'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@import_routes_bp.route("/import_csv", methods=["POST"])
def import_csv():
    #adapted from https://flask.palletsprojects.com/en/stable/patterns/fileuploads/
    
    # check if the post request has the file part
    if 'file' not in request.files:
        return "no file part"
    file = request.files['file']

    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        return 'No selected file'
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename) # type: ignore
        fullpath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(fullpath)

        import_alg.parse_csv(fullpath)
        return "success"
    
    return "file type not allowed"
    
@import_routes_bp.route("/import_status", methods=["POST"])
def import_status():
    # do something here
    return ""
from Modules.ImportAlgorithms import ImportAlgorithms
from Repositories.BudgetAndTransactionRepository import BudgetAndTransactionRepository
from Routes.AuthorisationRoutes import authorisation_bp
from Routes.AnalyticsRoutes import analytics_bp
from Routes.AlertsRoutes import alerts_bp
from Routes.ImportRoutes import import_routes_bp
from Routes.AdminRoutes import admin_bp

from flask import Flask, g
from flask_cors import CORS

# dbCon = 'dummy'
# repo = BudgetAndTransactionRepository(dbCon)
# import_module = ImportAlgorithms(repo)
# import_module.parse_csv("transactions.csv")


UPLOAD_FOLDER = '/path/to/the/uploads'

app = Flask(__name__)
CORS(app)


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(authorisation_bp)
app.register_blueprint(analytics_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(import_routes_bp)
app.register_blueprint(admin_bp)

app.run(debug=True)
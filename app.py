from flask import Flask
from flasgger import Swagger
from database.database import init_db
from routes.animals import register_animal_routes
from routes.owners import register_owner_routes
from routes.statistics_route import register_statistics_routes

flask_app = Flask(__name__)
swagger = Swagger(flask_app)

init_db()
register_animal_routes(flask_app)
register_owner_routes(flask_app)
register_statistics_routes(flask_app)

@flask_app.route("/")
def home():
    return "Hallo, das eine Tier-Api"

if __name__ == "__main__":
    flask_app.run(debug=True, port=5050)


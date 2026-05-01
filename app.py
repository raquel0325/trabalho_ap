from flask import Flask
from config import Config
from database.main import init_db

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Inicializa banco de dados
init_db()

# Registra Blueprints
from routes.auth import bp_auth
app.register_blueprint(bp_auth)

from routes.home import bp_home
app.register_blueprint(bp_home)

from routes.questionario import bp_questionario
app.register_blueprint(bp_questionario)

from routes.vagas import bp_vagas
app.register_blueprint(bp_vagas)

from routes.google_auth import bp_google, init_oauth
init_oauth(app)
app.register_blueprint(bp_google)

if __name__ == '__main__':
    app.run(debug=True)
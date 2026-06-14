from flask import Flask
from config import Config
from database import init_db  
from routes import bp_auth, bp_home, bp_questionario, bp_vagas, bp_google, init_oauth

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Inicializa banco de dados
init_db()

# Registra Blueprints
app.register_blueprint(bp_auth)
app.register_blueprint(bp_home)
app.register_blueprint(bp_questionario)
app.register_blueprint(bp_vagas)
init_oauth(app)
app.register_blueprint(bp_google)

if __name__ == '__main__':
    app.run(debug=True)
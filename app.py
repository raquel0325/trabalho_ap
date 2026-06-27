from flask import Flask
from config import Config
from database import init_db  
from routes import bp_auth, bp_home, bp_questionario, bp_vagas, bp_freelancer
from routes import bp_google, init_oauth, bp_candidatar_se, bp_atualizar_vaga
from routes import bp_avaliacao, bp_contratar_frelas, bp_atualizar_perfil, bp_solicitantes

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# Inicializa banco de dados
init_db()

# Registra Blueprints
app.register_blueprint(bp_auth)
app.register_blueprint(bp_home)
app.register_blueprint(bp_questionario)
app.register_blueprint(bp_vagas)
app.register_blueprint(bp_candidatar_se) 
app.register_blueprint(bp_atualizar_vaga)
app.register_blueprint(bp_freelancer)
app.register_blueprint(bp_avaliacao)
app.register_blueprint(bp_contratar_frelas)
app.register_blueprint(bp_atualizar_perfil)
app.register_blueprint(bp_solicitantes)
init_oauth(app)
app.register_blueprint(bp_google)

if __name__ == '__main__':
    app.run(debug=True)
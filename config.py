import os
from dotenv import load_dotenv

load_dotenv() # carrega variáveis de ambiente a partir de .env

class Config:
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'fallback-secret-key-bem-secret')
    #secret key 
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    #client id do google, obtido no google cloud
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    #client secret do google, obtido no google cloud
    GOOGLE_META_URL = "https://accounts.google.com/.well-known/openid-configuration"
    #url para obter o meta do google, usado no google auth
    
    # Database
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    #base dir do projeto
    DB_PATH = os.path.join(BASE_DIR, "database", "banco.db")
    #caminho para o banco de dados
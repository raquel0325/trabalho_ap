from flask import Blueprint, request, jsonify, session, render_template
from models.model_vagas import Vagas, Candidatura, Match, Competencia
from CRUDs.candidatura import CandidaturaCRUD
from CRUDs.crud_chat import ChatCRUD

bp_chat = Blueprint('chat', __name__)

@bp_chat.route('/chat/tela/<int:id_candidatura>', methods=['GET'])
def tela_chat(id_candidatura):
    return render_template('chat.html', id_candidatura=id_candidatura)

@bp_chat.route('/chat/<int:id_candidatura>/abrir', methods=['POST'])
def abrir_chat(id_candidatura):
    try:
        id_sala = ChatCRUD.liberar_chat(id_candidatura)
        return jsonify({"sucesso": True, "id_sala": id_sala, "mensagem": "Chat liberado!"}), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

@bp_chat.route('/chat/<int:id_candidatura>/enviar', methods=['POST'])
def enviar_mensagem(id_candidatura):
    dados = request.get_json()
    mensagem = dados.get('mensagem')
    
    # ATENÇÃO: No futuro, pegue esses IDs da 'session' do Flask (quem está logado)
    id_remetente = dados.get('id_remetente')
    tipo_remetente = dados.get('tipo_remetente') 

    try:
        ChatCRUD.enviar_mensagem(id_candidatura, id_remetente, tipo_remetente, mensagem)
        return jsonify({"sucesso": True}), 201
    except ValueError as e:
        return jsonify({"erro": str(e)}), 403 
    except Exception as e:
        return jsonify({"erro": "Erro no servidor."}), 500

@bp_chat.route('/chat/<int:id_candidatura>/mensagens', methods=['GET'])
def carregar_mensagens(id_candidatura):
    try:
        mensagens = ChatCRUD.carregar_mensagens(id_candidatura)
        return jsonify({"sucesso": True, "mensagens": mensagens}), 200
    except Exception as e:
        return jsonify({"erro": "Erro ao carregar o chat."}), 500
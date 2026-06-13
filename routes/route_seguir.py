from flask import Blueprint, request, session, jsonify
from models.model_seguir import Seguir

bp_seguir = Blueprint('seguir', __name__)


@bp_seguir.route('/seguir_usuario/<int:usuario_id>', methods=['POST'])
def seguir_usuario(usuario_id):
    """Segue um usuário"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    seguidor_id = session['usuario_id']
    
    try:
        sucesso = Seguir.seguir_usuario(seguidor_id, usuario_id)
        if sucesso:
            return jsonify({'success': True, 'message': 'Agora você está seguindo este usuário!'})
        else:
            return jsonify({'success': False, 'error': 'Já estava seguindo este usuário'}), 400
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp_seguir.route('/deixar_seguir/<int:usuario_id>', methods=['POST'])
def deixar_seguir(usuario_id):
    """Deixa de seguir um usuário"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    seguidor_id = session['usuario_id']
    
    try:
        sucesso = Seguir.deixar_seguir(seguidor_id, usuario_id)
        if sucesso:
            return jsonify({'success': True, 'message': 'Você deixou de seguir este usuário!'})
        else:
            return jsonify({'success': False, 'error': 'Você não seguia este usuário'}), 400
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp_seguir.route('/verificar_seguindo/<int:usuario_id>', methods=['GET'])
def verificar_seguindo(usuario_id):
    """Verifica se o usuário atual segue outro usuário"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    seguidor_id = session['usuario_id']
    
    try:
        seguindo = Seguir.verificar_seguindo(seguidor_id, usuario_id)
        return jsonify({'success': True, 'seguindo': seguindo})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp_seguir.route('/meus_seguidores', methods=['GET'])
def meus_seguidores():
    """Retorna lista de seguidores do usuário atual"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    usuario_id = session['usuario_id']
    
    try:
        seguidores = Seguir.listar_seguidores(usuario_id)
        seguidores_lista = [dict(seg) for seg in seguidores] if seguidores else []
        return jsonify({'success': True, 'seguidores': seguidores_lista})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp_seguir.route('/quem_sigo', methods=['GET'])
def quem_sigo():
    """Retorna lista de usuários que o atual segue"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    usuario_id = session['usuario_id']
    
    try:
        seguindo = Seguir.listar_seguindo(usuario_id)
        seguindo_lista = [dict(seg) for seg in seguindo] if seguindo else []
        return jsonify({'success': True, 'seguindo': seguindo_lista})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@bp_seguir.route('/estatisticas_seguidores', methods=['GET'])
def estatisticas_seguidores():
    """Retorna estatísticas de seguidores do usuário atual"""
    if 'usuario_id' not in session:
        return jsonify({'success': False, 'error': 'Não autorizado'}), 401
    
    usuario_id = session['usuario_id']
    
    try:
        estatisticas = Seguir.obrar_estatisticas(usuario_id)
        return jsonify({'success': True, 'estatisticas': estatisticas})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
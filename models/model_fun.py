from CRUDs.crud_func import FuncionarioCRUD
from CRUDs.crud_quest import QuestionarioCRUD
from models.model_comp import Competencia
from database.connect import get_connection

class Funcionario:
    
    @staticmethod
    def cadastrar(nome, email, senha, telefone, cpf):
        """Cadastra um novo funcionário com validações"""
        if not nome or len(nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        if not senha or len(senha) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        if not cpf or len(cpf) != 11:
            raise ValueError("CPF deve ter exatamente 11 dígitos")
        
        return FuncionarioCRUD.inserir(nome, email, senha, telefone, cpf)
    
    @staticmethod
    def autenticar(email, senha):
        """Autentica um funcionário"""
        funcionario = FuncionarioCRUD.buscar_por_email_senha(email, senha)
        if not funcionario:
            return None
        return {
            'id': funcionario['id_funcionario'],
            'nome': funcionario['nome'],
            'email': funcionario['email'],
            'tipo': 'funcionario'
        }
    
    @staticmethod
    def buscar_por_id(id_funcionario):
        """Busca funcionário por ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM funcionarios WHERE id_funcionario = ?', (id_funcionario,))
            return cursor.fetchone()
        finally:
            conn.close()
    
    @staticmethod
    def buscar_por_google(email):
        """Busca funcionário via Google"""
        funcionario = FuncionarioCRUD.buscar_por_email(email)
        if not funcionario:
            return None
        return {
            'id': funcionario['id_funcionario'],
            'nome': funcionario['nome'],
            'email': funcionario['email'],
            'telefone': funcionario['telefone'],
            'cpf': funcionario['cpf']
        }
    
    @staticmethod
    def cadastrar_via_google(nome, email):
        """Cadastra funcionário via Google"""
        return FuncionarioCRUD.inserir(nome, email, 'google_oauth', '', '')
    
    @staticmethod
    def verificar_dados_incompletos(id_funcionario):
        """Verifica se faltam dados no perfil"""
        func = Funcionario.buscar_por_id(id_funcionario)
        if func:
            return not (func['telefone'] and func['cpf'])
        return True
    
    @staticmethod
    def obter_perfil_completo(id_funcionario):
        """Obtém perfil completo com questionário"""
        funcionario = Funcionario.buscar_por_id(id_funcionario)
        if not funcionario:
            return None
        
        questionario = QuestionarioCRUD.buscar_por_funcionario(id_funcionario)
        competencias = Competencia.listar_do_funcionario(id_funcionario)
        
        return {
            'id': funcionario['id_funcionario'],
            'nome': funcionario['nome'],
            'email': funcionario['email'],
            'telefone': funcionario['telefone'],
            'cpf': funcionario['cpf'],
            'questionario': questionario,
            'competencias': competencias
        }
    
    @staticmethod
    def atualizar_perfil(id_funcionario, nome=None, telefone=None, cpf=None):
        """Atualiza dados do perfil"""
        return FuncionarioCRUD.atualizar(id_funcionario, nome, telefone, cpf)
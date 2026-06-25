from CRUDs.crud_emp import EmpresaCRUD
import re

class Empresa:
    
    @staticmethod
    def cadastrar(nome, cnpj, email, senha, telefone='', endereco=''):
        """Cadastra uma nova empresa com validações"""
        # Validações
        cnpj = re.sub(r'\D', '', cnpj) if cnpj else ''
        telefone = re.sub(r'\D', '', telefone) if telefone else ''
        if not nome or len(nome) < 2:
            raise ValueError("Nome da empresa deve ter pelo menos 2 caracteres")
        
        if len(cnpj) != 14:
            raise ValueError("CNPJ deve ter 14 dígitos")
        
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        if not senha or len(senha) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        
        return EmpresaCRUD.inserir(nome, cnpj, email, senha, telefone, endereco)
    
    @staticmethod
    def autenticar(email, senha):
        """Autentica uma empresa"""
        empresa = EmpresaCRUD.buscar_por_email_senha(email, senha)
        
        if not empresa:
            return None
        
        return {
            'id': empresa['id_empresa'],
            'nome': empresa['nome'],
            'email': empresa['email'],
            'cnpj': empresa['cnpj'],
            'tipo': 'empresa'
        }
    @staticmethod
    def buscar_por_id(id_empresa):
        """Busca empresa por ID"""
        return EmpresaCRUD.buscar_por_id(id_empresa)
    @staticmethod
    def atualizar_perfil(id_empresa, nome=None, email=None, telefone=None, endereco=None):
        """Atualiza o perfil da empresa com validações"""
        if email and '@' not in email:
            raise ValueError("Email inválido")
        
        if nome and len(nome) < 2:
            raise ValueError("Nome da empresa deve ter pelo menos 2 caracteres")
        
        return EmpresaCRUD.atualizar(id_empresa, nome, email, telefone, endereco)
#======================================================================================================================================
    @staticmethod
    def excluir_perfil(id_empresa):
        return EmpresaCRUD.deletar(id_empresa)
from CRUDs.crud_emp import EmpresaCRUD
import re

class Empresa:
    
    @staticmethod
    def cadastrar(nome, cnpj, email, senha, telefone='', endereco=''):
        """Cadastra uma nova empresa com validações"""
        # Validações
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
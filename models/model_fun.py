from CRUDs.crud_func import FuncionarioCRUD

class Funcionario:
   
    
    @staticmethod
    def cadastrar(nome, email, senha, telefone, cpf):
        """Cadastra um novo funcionário com validações"""
        # Validações de negócio
        if not nome or len(nome) < 3:
            raise ValueError("Nome deve ter pelo menos 3 caracteres")
        
        if not email or '@' not in email:
            raise ValueError("Email inválido")
        
        if not senha or len(senha) < 6:
            raise ValueError("Senha deve ter pelo menos 6 caracteres")
        if not cpf or len(cpf) != 11:
            raise ValueError("CPF deve ter exatamente 11 dígitos")
        
        # Se passou nas validações, chama o CRUD
        return FuncionarioCRUD.inserir(nome, email, senha, telefone, cpf)
    
    @staticmethod
    def autenticar(email, senha):
        """Autentica um funcionário"""
        funcionario = FuncionarioCRUD.buscar_por_email_senha(email, senha)
        
        if not funcionario:
            return None
        
        # Formata os dados para o formato que o sistema usa
        return {
            'id': funcionario['id_funcionario'],
            'nome': funcionario['nome'],
            'email': funcionario['email'],
            'tipo': 'funcionario'
        }
    
    @staticmethod
    def buscar_por_google(email):
        """Busca ou cria funcionário via Google"""
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
        """Cadastra funcionário via Google (sem senha)"""
        # Insere com senha padrão e dados vazios
        return FuncionarioCRUD.inserir(
            nome=nome,
            email=email,
            senha='google_oauth',
            telefone='',
            cpf=''
        )
    
    @staticmethod
    def verificar_dados_incompletos(id_funcionario):
        func = FuncionarioCRUD.buscar_por_id(id_funcionario)
        if func:
            return not (func['telefone'] and func['cpf'])
        return True
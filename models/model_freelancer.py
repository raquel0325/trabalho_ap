from CRUDs.crud_freelancer import FreelancerCRUD

class Freelancer:

    @staticmethod
    def buscar_freelancer(busca=None, disponibilidade=None, preco_medio_min=None, preco_medio_max=None):
        """Busca freelancers com filtros opcionais"""
        filtros = {}
        
        if busca:
            filtros['busca'] = busca
        if disponibilidade:
            filtros['disponibilidade'] = disponibilidade
        if preco_medio_min is not None:
            filtros['preco_medio_min'] = preco_medio_min
        if preco_medio_max is not None:
            filtros['preco_medio_max'] = preco_medio_max
        
        return FreelancerCRUD.buscar_freelancer(filtros)

    @staticmethod
    def listar_por_funcionario(id_funcionario):
        """Lista todos os freelances de um funcionário"""
        return FreelancerCRUD.listar_por_funcionario(id_funcionario)
    @staticmethod
    def buscar_por_funcionario(id_funcionario):
        """Busca um freelance pelo ID do funcionário"""
        return FreelancerCRUD.buscar_por_funcionario(id_funcionario)


    
from CRUDs.crud_contratar import ContratacaoCRUD

class Contratacao:
    @staticmethod
    def contratar_freelancer(id_freelancer, id_contratante, tipo_contratante):
        return ContratacaoCRUD.contratar_freelancer(
            id_freelancer,
            id_contratante,
            tipo_contratante,
            
        )
    @staticmethod
    def buscar_por_freelancer_e_contratante(id_freelancer, id_contratante, tipo_contratante):
        return ContratacaoCRUD.buscar_por_freelancer_e_contratante(
            id_freelancer,
            id_contratante,
            tipo_contratante
        )
    @staticmethod
    def listar_contratacao(id_funcionario):
        return ContratacaoCRUD.listar_contratacao(id_funcionario)
    
    @staticmethod
    def listar_contratados(id_contratante):
        return ContratacaoCRUD.listar_contratados(id_contratante)
    @staticmethod
    def atualizar_status(id_contratacao, novo_status, id_freelancer_dono):
        """Atualiza o status de uma contratação (chamado pelo dono do freelancer)"""
        return ContratacaoCRUD.atualizar_status(id_contratacao, novo_status, id_freelancer_dono)

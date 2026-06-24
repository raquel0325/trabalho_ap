from CRUDs.crud_contratar import ContratacaoCRUD

class Contratacao:
    @staticmethod
    def contratar_freelancer(id_freelancer, id_contratante):
        return ContratacaoCRUD.contratar_freelancer(
            id_freelancer,
            id_contratante
        )
    @staticmethod
    def listar_contratacao(id_funcionario):
        return ContratacaoCRUD.listar_contratacao(id_funcionario)
    
    @staticmethod
    def listar_contratados(id_contratante):
        return ContratacaoCRUD.listar_contratados(id_contratante)
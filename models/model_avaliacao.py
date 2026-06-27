from CRUDs.crud_avaliacao import AvaliacaoCRUD

class Avaliacao:
    @staticmethod
    def adicionar_avaliacao(id_freelancer, id_contratante, tipo_contratante, nota, comentario):
       """Adiciona uma avaliação para um freelancer"""
       return AvaliacaoCRUD.adicionar_avaliacao(id_freelancer, id_contratante, tipo_contratante, nota, comentario)
    
    @staticmethod
    def calcular_media_avaliacoes(id_freelancer):
        """Calcula a média das avaliações"""
        return AvaliacaoCRUD.calcular_media_avaliacoes(id_freelancer)
    
    @staticmethod
    def listar_avaliacoes_com_usuarios(id_freelancer):
        """Lista avaliações com dados dos avaliadores"""
        return AvaliacaoCRUD.listar_avaliacoes_com_usuarios(id_freelancer)
    
from CRUDs.crud_comp import CompetenciaCRUD

class Competencia:
    """Classe que contém as regras de negócio para competências"""
    
    @staticmethod
    def listar_todas():
        """Lista todas as competências disponíveis"""
        return CompetenciaCRUD.listar_todas()
    
    @staticmethod
    def adicionar_ao_funcionario(id_funcionario, nome_competencia):
        """Adiciona uma competência ao funcionário (cria se não existir)"""
        # Busca ou cria a competência
        competencia = CompetenciaCRUD.buscar_por_nome(nome_competencia)
        
        if not competencia:
            comp_id = CompetenciaCRUD.inserir(nome_competencia)
        else:
            comp_id = competencia['id_competencia']
        
        # Vincula ao funcionário
        CompetenciaCRUD.vincular_funcionario(id_funcionario, comp_id)
        return comp_id
    
    @staticmethod
    def listar_do_funcionario(id_funcionario):
        """Lista competências de um funcionário"""
        return CompetenciaCRUD.listar_do_funcionario(id_funcionario)
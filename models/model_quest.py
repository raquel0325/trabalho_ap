from CRUDs.crud_quest import QuestionarioCRUD
from models.model_comp import Competencia

class Questionario:
    """Classe que contém as regras de negócio para o questionário"""
    
    @staticmethod
    def salvar(id_funcionario, dados, competencias_ids, novas_competencias):
        """Salva o questionário completo com validações"""
        # Validações
        campos_obrigatorios = ['cidade', 'estado', 'formacao', 'ultimo_cargo', 
                              'ultima_empresa', 'tempo_experiencia']
        
        for campo in campos_obrigatorios:
            if not dados.get(campo):
                raise ValueError(f"Campo {campo} é obrigatório")
        
        # Salva resposta do questionário
        QuestionarioCRUD.inserir_resposta(
            id_funcionario=id_funcionario,
            cidade=dados.get('cidade'),
            estado=dados.get('estado'),
            formacao=dados.get('formacao'),
            curso=dados.get('curso', ''),
            instituicao=dados.get('instituicao', ''),
            ano_conclusao=dados.get('ano_conclusao'),
            ultimo_cargo=dados.get('ultimo_cargo'),
            ultima_empresa=dados.get('ultima_empresa'),
            tempo_experiencia=dados.get('tempo_experiencia')
        )
        
        # Vincula competências existentes
        for comp_id in competencias_ids:
            Competencia.adicionar_ao_funcionario(id_funcionario, comp_id)
        
        # Adiciona novas competências
        for nome_comp in novas_competencias:
            if nome_comp.strip():
                Competencia.adicionar_ao_funcionario(id_funcionario, nome_comp.strip())
        
        return True
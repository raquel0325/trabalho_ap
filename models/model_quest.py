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
        
        # Vincula competências existentes (são IDs)
        for comp_id in competencias_ids:
            if comp_id:  # Verifica se o ID não está vazio
                try:
                    # O método adicionar_ao_funcionario agora aceita tanto ID quanto nome
                    Competencia.adicionar_ao_funcionario(id_funcionario, int(comp_id))
                except Exception as e:
                    print(f"Erro ao adicionar competência ID {comp_id}: {e}")
                    continue
        
        # Adiciona novas competências (são nomes)
        for nome_comp in novas_competencias:
            if nome_comp.strip():
                Competencia.adicionar_ao_funcionario(id_funcionario, nome_comp.strip())
        
        return True
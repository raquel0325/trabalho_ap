from CRUDs.crud_vagas import VagaCRUD
from CRUDs.candidatura import CandidaturaCRUD, MatchCRUD
from CRUDs.crud_comp import CompetenciaCRUD
import re

class Vaga:
    @staticmethod
    def criar(titulo, descricao, salario, cidade, regime, id_empresa, competencias_ids):
        """Cria uma nova vaga com validações"""
        if not titulo or len(titulo) < 3:
            raise ValueError("Título deve ter pelo menos 3 caracteres")
        if not descricao or len(descricao) < 50:

            raise ValueError("Descrição deve ter pelo menos 50 caracteres")
        if salario and salario < 0:

            raise ValueError("Salário não pode ser negativo")
        if not competencias_ids:

            raise ValueError("Selecione pelo menos uma competência")
        
        return VagaCRUD.inserir(titulo, descricao, salario, cidade, regime, id_empresa, competencias_ids)
#'''========================================================================='''


    @staticmethod
    def listar_empresa(id_empresa):
        """Lista vagas de uma empresa"""
        return VagaCRUD.listar_por_empresa(id_empresa)
    

#'''========================================================================='''

    @staticmethod
    def buscar(id_vaga):
        """Busca uma vaga específica"""
        vaga = VagaCRUD.buscar_por_id(id_vaga)
        if vaga:
            competencias = VagaCRUD.buscar_competencias_vaga(id_vaga)
            vaga_dict = dict(vaga)
            vaga_dict['competencias'] = competencias
            return vaga_dict
        return None
    
    @staticmethod
    def atualizar(id_vaga, titulo=None, descricao=None, salario=None):
        """Atualiza uma vaga"""
        return VagaCRUD.atualizar(id_vaga, titulo, descricao, salario)
    
    @staticmethod
    def deletar(id_vaga):
        """Remove uma vaga"""
        return VagaCRUD.deletar(id_vaga)
    
    @staticmethod
    def listar_todas(busca=None, salario_min=None, empresa=None, filtros=None):
        """Lista todas as vagas com filtros"""
        if filtros is None:
            filtros = {
                'busca': busca,
                'salario_min': salario_min,
                'empresa': empresa
        }
        return VagaCRUD.listar_todas(filtros)


class Candidatura:
    """Regras para candidaturas"""
    
    @staticmethod
    def candidatar(id_funcionario, id_vaga):
        """Registra candidatura"""
        if CandidaturaCRUD.verificar_candidatura(id_funcionario, id_vaga):
            raise ValueError("Você já se candidatou a esta vaga!")
        return CandidaturaCRUD.candidatar(id_funcionario, id_vaga)
    
    @staticmethod
    def listar_do_funcionario(id_funcionario):
        """Lista candidaturas do funcionário"""
        return CandidaturaCRUD.listar_candidaturas_funcionario(id_funcionario)
    
    @staticmethod
    def listar_da_vaga(id_vaga):
        """Lista candidatos de uma vaga"""
        return CandidaturaCRUD.listar_candidatos_vaga(id_vaga)

class Match:
    """Regras para match"""
    @staticmethod
    def calcular(id_funcionario, id_vaga):
        """Só valida/chama o CRUD"""
        if id_funcionario <= 0 or id_vaga <= 0:
            return 0
        return MatchCRUD.calcular(id_funcionario, id_vaga)
    
    
    @staticmethod
    def melhores_vagas(id_funcionario, limite=20):
        if id_funcionario <= 0:
            return []
        return MatchCRUD.listar_melhores(id_funcionario, limite)
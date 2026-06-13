from CRUDs.crud_seguir import SeguirCRUD


class Seguir:
    """Regras de negócio para seguir usuários"""
    
    @staticmethod
    def seguir_usuario(seguidor_id, seguido_id):
        """Segue um usuário com validações"""
        if seguidor_id == seguido_id:
            raise ValueError("Não é possível seguir a si mesmo!")
        
        return SeguirCRUD.seguir(seguidor_id, seguido_id)
    
    @staticmethod
    def deixar_seguir(seguidor_id, seguido_id):
        """Deixa de seguir um usuário"""
        return SeguirCRUD.deixar_seguir(seguidor_id, seguido_id)
    
    @staticmethod
    def verificar_seguindo(seguidor_id, seguido_id):
        """Verifica se segue um usuário"""
        return SeguirCRUD.verificar_seguindo(seguidor_id, seguido_id)
    
    @staticmethod
    def listar_seguidores(usuario_id):
        """Lista seguidores de um usuário"""
        return SeguirCRUD.listar_seguidores(usuario_id)
    
    @staticmethod
    def listar_seguindo(usuario_id):
        """Lista usuários que um usuário segue"""
        return SeguirCRUD.listar_seguindo(usuario_id)
    
    @staticmethod
    def obrar_estatisticas(usuario_id):
        """Retorna estatísticas de seguidores"""
        return {
            'seguidores': SeguirCRUD.contar_seguidores(usuario_id),
            'seguindo': SeguirCRUD.contar_seguindo(usuario_id)
        }
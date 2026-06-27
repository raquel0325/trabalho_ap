from CRUDs.crud_notificacao import NotificacaoCRUD


class Notificacao:
    @staticmethod
    def criar(id_usuario: int, titulo: str, mensagem: str, tipo: str, id_referencia: int | None = None):
        return NotificacaoCRUD.inserir(
            id_usuario=id_usuario,
            titulo=titulo,
            mensagem=mensagem,
            tipo=tipo,
            id_referencia=id_referencia,
        )

    @staticmethod
    def listar_para_usuario(id_usuario: int, apenas_nao_lidas = False, limite: int = 20):
        return NotificacaoCRUD.listar_por_usuario(id_usuario, apenas_nao_lidas=apenas_nao_lidas, limite=limite)

    
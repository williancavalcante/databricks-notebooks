import json
from heimdall.base_message_sender import JaimeMessage
from heimdall.base_message_sender import BaseMessageFormatter
from heimdall.base_message_sender import MessageSender
from heimdall.storage_context import StorageContext

class HeimdallStorage:
    """
    Fachada que integra a gestão de contexto de armazenamento e envio de mensagens. (Conceito de composição de classes - Desing Pattern Facade)

    Attributes:
        jaime (JaimeMessage): Gestor de mensagens.
        attributes (StorageContext): Atributos de contexto Storage

    Args:
            storage_account (str): Conta de armazenamento.
            path (str): Caminho associado à ação de gatilho.
            blob (str): Nome do blob no contexto de armazenamento.
            invocation_id (str): ID de invocação do processo.
            notification (str): Identificador ou canal de notificação.
            run_context (str): Json string contento o contexto da execução (run_id, job_id, workspace_id, etc.)
    """
    def __init__(self, storage_account: str, path: str, blob: str, invocation_id: str, notification: str, run_context: str):
        self.attributes     = StorageContext(storage_account, path, blob, invocation_id)
        self.run_context    = convert_json_string_in_obj(run_context)
        __formatter         = BaseMessageFormatter(invocation_id, path, blob, self.attributes.user_request)
        __sender            = MessageSender(notification)
        self.jaime          = JaimeMessage(__formatter, __sender) #Classe dependente do contexto de outras classes (Injeção de dependencia)


def convert_json_string_in_obj(json_string):
    """
    Função que recebe como parametro um json string e retorna como um objeto dict

    :param json_string (str): conteudo do tipo json string

    Returns:
        json_obj (dict): conteudo do tipo dict
    """
    json_obj = json.loads(json_string)
    return json_obj
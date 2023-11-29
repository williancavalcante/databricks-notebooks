import ast
from typing import Type
from jaiminho import jaiminho

class BaseMessageFormatter:
    """
    Formata uma mensagem base que inclui o ID de invocação, ação de gatilho e nome do arquivo.

    Attributes:
        _invocation_id (str): ID de invocação do processo.
        _path (str): Caminho associado à ação de gatilho.
        _file (str): Nome do arquivo envolvido no processo.
        _user_request (str): Nome do usuário que disparou disparou o evento.
    """
    def __init__(self, invocation_id: str, path: str, file: str, user_request: str) -> str:
        self._invocation_id = invocation_id
        self._path          = path
        self._file          = file
        self._user_request  = user_request

    def base_message(self):
        """
        Constrói a mensagem base.

        Returns:
            str: Mensagem base formatada.
        """
        return (
            f"**Invocation ID**: {self._invocation_id}\n\n"
            f"**Trigger Action**: {self._path}\n\n"
            f"**Nome do Arquivo**: {self._file}\n\n"
            f"**Requisitado por**: {self._user_request}\n\n"
        )


class MessageSender:
    """
    Responsável por enviar mensagens usando um serviço de notificação externo.

    Attributes:
        _notification (list[str]): Canal de notificação para o qual a mensagem será enviada.
    """
    def __init__(self, notification: str) -> None:
        self._notification = ast.literal_eval(notification)

    def send_message(self, message: str) -> str:
        """
        Envia a mensagem fornecida para o canal de notificação configurado.

        Args:
            message (str): A mensagem a ser enviada.
        """
        return jaiminho.post_message(self._notification, message=message)

class JaimeMessage:
    """
    Gerencia a formatação e o envio de mensagens informativas, de sucesso e de erro.

    Attributes:
        _formatter (BaseMessageFormatter): Formatador para a mensagem base.
        _sender (MessageSender): Remetente para enviar a mensagem.
    """
    def __init__(self, formatter: Type[BaseMessageFormatter], sender: Type[MessageSender]) -> None:
        self._formatter = formatter
        self._sender    = sender

    def _format_dict_message(self, message_dict=None) -> str:
        """
        Formata um dicionário de mensagens em uma string.

        Args:
            message_dict (dict): Dicionário contendo pares chave-valor para a mensagem.

        Returns:
            str: Mensagem formatada.
        """
        if message_dict is None:
            return ""

        formatted_message = ""
        for key, value in message_dict.items():
            if value is not None:
                formatted_message += f"**{key}**: {value}\n\n"
        
        return formatted_message

    def send_info_message(self, titulo: str, custom_message=None) -> str:
        """
        Envia uma mensagem informativa com um título e uma mensagem personalizada.

        Args:
            titulo (str): Título da mensagem informativa.
            custom_message (dict): Mensagem personalizada em formato de dicionário.
        """
        common_message              = self._formatter.base_message()
        formatted_custom_message    = self._format_dict_message(custom_message)
        full_message                = f"ℹ️ **{titulo}**\n\n" + '_'*30 + "\n\n" + common_message + formatted_custom_message
        self._sender.send_message(full_message)

    def send_sucess_message(self, titulo: str, custom_message=None) -> str:
        """
        Envia uma mensagem de sucesso com um título e uma mensagem personalizada.

        Args:
            titulo (str): Título da mensagem de sucesso.
            custom_message (dict): Mensagem personalizada em formato de dicionário.
        """
        common_message              = self._formatter.base_message()
        formatted_custom_message    = self._format_dict_message(custom_message)
        full_message                = f"✅ **{titulo}**\n\n" + '_'*30 + "\n\n" + common_message + formatted_custom_message
        self._sender.send_message(full_message)

    def send_error_message(self, titulo: str, custom_message=None) -> str:
        """
        Envia uma mensagem de erro com um título e uma mensagem personalizada.

        Args:
            titulo (str): Título da mensagem de erro.
            custom_message (dict): Mensagem personalizada em formato de dicionário.
        """
        common_message              = self._formatter.base_message()
        formatted_custom_message    = self._format_dict_message(custom_message)
        full_message                = f"🚨 **{titulo}**\n\n" + '_'*30 + "\n\n" + common_message + formatted_custom_message
        self._sender.send_message(full_message)
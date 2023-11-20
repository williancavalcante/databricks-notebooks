import re

class StorageContext:
    """
    Gerencia e fornece contexto de armazenamento, como conta de armazenamento,
    ID de invocação, informações do contêiner e do blob.

    Attributes:
        storage_account (str): Conta de armazenamento utilizada.
        invocation_id (str): ID de invocação do processo.
        container (str): Nome do contêiner no contexto de armazenamento.
        path (str): Caminho do arquivo.
        blob (str): Nome do blob no contexto de armazenamento.
    """

    def __init__(self, storage_account: str, path: str, blob: str, invocation_id: str) -> None:
        self.storage_account    = storage_account
        self.invocation_id      = invocation_id
        self.container          = self._extract_value(re.compile(r"containers/([^/]+)"), path)
        self.path               = self._extract_value(re.compile(r"blobs/(.+)"), path)
        self.blob               = blob
        self.abfss              = f"abfss://{self.container}@{self.storage_account}.dfs.core.windows.net/{self.path}{self.blob}"
        self.user_request       = self._extract_value(re.compile(r"(?:[^_]*_){6}([^\.]+)"), blob)

    @staticmethod
    def _extract_value(pattern: str, text: str) -> str:
        """
        Extrai um valor com base em um padrão regex fornecido.

        Args:
            pattern (str): O padrão regex para extração.
            text (str): O texto do qual extrair o valor.

        Returns:
            str: O valor extraído ou uma string vazia se nenhuma correspondência for encontrada.
        """
        match = re.search(pattern, text)
        return match.group(1) if match else ""
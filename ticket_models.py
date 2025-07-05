from abc import ABC, abstractmethod
from datetime import datetime

class Ticket(ABC):
    """Classe abstrata que representa um ticket genérico."""
    def __init__(self, codigo_colaborador: str, tipo: str):
        if not codigo_colaborador:
            raise ValueError("Código de colaborador não pode ser vazio.")
        if tipo not in ['hardware', 'software']:
            raise ValueError("Tipo deve ser 'hardware' ou 'software'.")
        self.codigo_colaborador = codigo_colaborador
        self.tipo = tipo
        self.data_hora_criacao = datetime.now()
        self.estado = "porAtender"

    @abstractmethod
    def atender_ticket(self):
        pass

class HardwareTicket(Ticket):
    def __init__(self, codigo_colaborador: str, equipamento: str, avaria: str):
        super().__init__(codigo_colaborador, 'hardware')
        if not equipamento or not avaria:
            raise ValueError("Equipamento e avaria não podem ser vazios.")
        self.equipamento = equipamento
        self.avaria = avaria
        self.data_hora_atendimento = None
        self.descricao_reparacao = ""
        self.pecas = []
        self.estado_atendimento = "em espera"

    def atender_ticket(self, descricao_reparacao: str, pecas: list):
        self.data_hora_atendimento = datetime.now()
        self.descricao_reparacao = descricao_reparacao
        self.pecas = pecas
        self.estado_atendimento = "atendido"

class SoftwareTicket(Ticket):
    def __init__(self, codigo_colaborador: str, software: str, descricao_necessidade: str):
        super().__init__(codigo_colaborador, 'software')
        if not software or not descricao_necessidade:
            raise ValueError("Software e descrição da necessidade não podem ser vazios.")
        self.software = software
        self.descricao_necessidade = descricao_necessidade
        self.data_hora_atendimento = None
        self.descricao_intervencao = ""
        self.estado_atendimento = "em espera"

    def atender_ticket(self, descricao_intervencao: str):
        self.data_hora_atendimento = datetime.now()
        self.descricao_intervencao = descricao_intervencao
        self.estado_atendimento = "atendido"

class Usuario:
    def __init__(self, usuario_id: int, username: str, tipo: str):
        self.usuario_id = usuario_id
        self.username = username
        self.tipo = tipo
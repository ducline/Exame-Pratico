from abc import ABC, abstractmethod
from datetime import datetime

# classe abstrata para ticket
class Ticket(ABC):
    # inicializa ticket
    def __init__(self, codigo_colaborador: str, tipo: str):
        if not codigo_colaborador:
            raise ValueError("código de colaborador não pode ser vazio.")
        if tipo not in ['hardware', 'software']:
            raise ValueError("tipo deve ser 'hardware' ou 'software'.")
        self.codigo_colaborador = codigo_colaborador
        self.tipo = tipo
        self.data_hora_criacao = datetime.now()
        self.estado = "porAtender"

    # método abstrato para atender ticket
    @abstractmethod
    def atender_ticket(self):
        pass

# classe para ticket de hardware
class HardwareTicket(Ticket):
    # inicializa hardware ticket
    def __init__(self, codigo_colaborador: str, equipamento: str, avaria: str):
        super().__init__(codigo_colaborador, 'hardware')
        if not equipamento or not avaria:
            raise ValueError("equipamento e avaria não podem ser vazios.")
        self.equipamento = equipamento
        self.avaria = avaria
        self.data_hora_atendimento = None
        self.descricao_reparacao = ""
        self.pecas = []
        self.estado_atendimento = "em espera"

    # atende hardware ticket
    def atender_ticket(self, descricao_reparacao: str, pecas: list):
        self.data_hora_atendimento = datetime.now()
        self.descricao_reparacao = descricao_reparacao
        self.pecas = pecas
        self.estado_atendimento = "atendido"

# classe para ticket de software
class SoftwareTicket(Ticket):
    # inicializa software ticket
    def __init__(self, codigo_colaborador: str, software: str, descricao_necessidade: str):
        super().__init__(codigo_colaborador, 'software')
        if not software or not descricao_necessidade:
            raise ValueError("software e descrição da necessidade não podem ser vazios.")
        self.software = software
        self.descricao_necessidade = descricao_necessidade
        self.data_hora_atendimento = None
        self.descricao_intervencao = ""
        self.estado_atendimento = "em espera"

    # atende software ticket
    def atender_ticket(self, descricao_intervencao: str):
        self.data_hora_atendimento = datetime.now()
        self.descricao_intervencao = descricao_intervencao
        self.estado_atendimento = "atendido"

# classe para utilizador
class Usuario:
    # inicializa utilizador
    def __init__(self, usuario_id: int, username: str, tipo: str):
        self.usuario_id = usuario_id
        self.username = username
        self.tipo = tipo
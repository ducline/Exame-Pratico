import pyodbc
import hashlib
from datetime import datetime
from ticket_models import HardwareTicket, SoftwareTicket, Usuario

# string de ligação à base de dados
CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HP_LAPTOP_DAN\\SQLEXPRESS;"
    "DATABASE=db_ticket2help;"
    "UID=user_ticket;"
    "PWD=user_ticket;"
    "TrustServerCertificate=Yes;"
    "Encrypt=No;"
)

# faz hash à password
def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

# autentica utilizador
def autenticar_usuario(username, password):
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute("SELECT UsuarioID, Username, PasswordHash, Tipo FROM Usuario WHERE Username = ?", username)
    user = cursor.fetchone()
    conn.close()
    if user and user.PasswordHash == hash_password(password):
        return Usuario(user.UsuarioID, user.Username, user.Tipo)
    return None

# insere ticket na base de dados
def inserir_ticket(ticket):
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO Ticket (CodigoColaborador, Tipo, DataHoraCriacao, Estado) OUTPUT INSERTED.TicketID VALUES (?, ?, ?, ?)",
        ticket.codigo_colaborador, ticket.tipo, ticket.data_hora_criacao, ticket.estado
    )
    ticket_id = cursor.fetchone()[0]
    if isinstance(ticket, HardwareTicket):
        cursor.execute(
            "INSERT INTO HardwareTicket (TicketID, Equipamento, Avaria, EstadoAtendimento) VALUES (?, ?, ?, ?)",
            ticket_id, ticket.equipamento, ticket.avaria, ticket.estado_atendimento
        )
    elif isinstance(ticket, SoftwareTicket):
        cursor.execute(
            "INSERT INTO SoftwareTicket (TicketID, Software, DescricaoNecessidade, EstadoAtendimento) VALUES (?, ?, ?, ?)",
            ticket_id, ticket.software, ticket.descricao_necessidade, ticket.estado_atendimento
        )
    conn.commit()
    conn.close()

# lista todos os tickets
def listar_tickets():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute("SELECT TicketID, CodigoColaborador, Tipo, DataHoraCriacao, Estado FROM Ticket")
    for row in cursor.fetchall():
        print(f"\nTicketID: {row.TicketID}, Tipo: {row.Tipo}, Código Colaborador: {row.CodigoColaborador}, Data Criação: {row.DataHoraCriacao}, Estado: {row.Estado}")
        if row.Tipo == 'hardware':
            cursor.execute("SELECT Equipamento, Avaria FROM HardwareTicket WHERE TicketID = ?", row.TicketID)
            hw = cursor.fetchone()
            if hw:
                print(f"  Equipamento: {hw.Equipamento}, Avaria: {hw.Avaria}")
        elif row.Tipo == 'software':
            cursor.execute("SELECT Software, DescricaoNecessidade FROM SoftwareTicket WHERE TicketID = ?", row.TicketID)
            sw = cursor.fetchone()
            if sw:
                print(f"  Software: {sw.Software}, Descrição Necessidade: {sw.DescricaoNecessidade}")
    conn.close()

# lista tickets por atender
def listar_tickets_por_atender():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    cursor.execute("SELECT TicketID, Tipo FROM Ticket WHERE Estado = 'porAtender'")
    tickets = cursor.fetchall()
    conn.close()
    return tickets

# atende um ticket
def atender_ticket():
    tickets = listar_tickets_por_atender()
    if not tickets:
        print("Não há tickets por atender.")
        return
    print("\nTickets por atender:")
    for idx, t in enumerate(tickets, 1):
        print(f"{idx} - TicketID: {t.TicketID}, Tipo: {t.Tipo}")
    try:
        escolha = int(input("Escolha o número do ticket para atender: "))
        if escolha < 1 or escolha > len(tickets):
            print("Escolha inválida.")
            return
    except ValueError:
        print("Entrada inválida.")
        return
    ticket = tickets[escolha - 1]
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    if ticket.Tipo == 'hardware':
        descricao = input("Descrição da reparação: ")
        pecas = input("Peças usadas (separadas por vírgula): ")
        data_atendimento = datetime.now()
        cursor.execute(
            "UPDATE HardwareTicket SET DescricaoReparacao=?, Pecas=?, DataHoraAtendimento=?, EstadoAtendimento='atendido' WHERE TicketID=?",
            descricao, pecas, data_atendimento, ticket.TicketID
        )
    elif ticket.Tipo == 'software':
        descricao = input("Descrição da intervenção: ")
        data_atendimento = datetime.now()
        cursor.execute(
            "UPDATE SoftwareTicket SET DescricaoIntervencao=?, DataHoraAtendimento=?, EstadoAtendimento='atendido' WHERE TicketID=?",
            descricao, data_atendimento, ticket.TicketID
        )
    cursor.execute(
        "UPDATE Ticket SET Estado='atendido' WHERE TicketID=?",
        ticket.TicketID
    )
    conn.commit()
    conn.close()
    print("Ticket atendido com sucesso.")
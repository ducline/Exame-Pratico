import getpass
from ticket_controller import autenticar_usuario, inserir_ticket, listar_tickets, atender_ticket
from ticket_models import HardwareTicket, SoftwareTicket

# mostra menu principal
def menu_principal():
    while True:
        print("\n1 - login")
        print("2 - sair")
        opcao = input("opção: ")
        if opcao == "1":
            login()
        elif opcao == "2":
            print("a sair...")
            break
        else:
            print("opção inválida")

# faz login do utilizador
def login():
    username = input("username: ")
    password = getpass.getpass("password: ")
    user = autenticar_usuario(username, password)
    if user:
        print(f"bem-vindo, {user.username} ({user.tipo})")
        menu_utilizador(user)
    else:
        print("login inválido")

# mostra menu do utilizador
def menu_utilizador(user):
    while True:
        print("\n1 - criar ticket")
        print("2 - listar tickets")
        if user.tipo == "tecnico":
            print("3 - atender ticket")
        print("0 - sair")
        opcao = input("opção: ")
        if opcao == "1":
            criar_ticket(user)
        elif opcao == "2":
            listar_tickets()
        elif opcao == "3" and user.tipo == "tecnico":
            atender_ticket()
        elif opcao == "0":
            break
        else:
            print("opção inválida")

# cria novo ticket
def criar_ticket(user):
    print("\n1 - hardware")
    print("2 - software")
    tipo = input("tipo de ticket: ")
    if tipo == "1":
        equipamento = input("equipamento: ")
        avaria = input("avaria: ")
        ticket = HardwareTicket(user.username, equipamento, avaria)
    elif tipo == "2":
        software = input("software: ")
        descricao = input("descrição da necessidade: ")
        ticket = SoftwareTicket(user.username, software, descricao)
    else:
        print("tipo inválido")
        return
    inserir_ticket(ticket)
    print("ticket criado com sucesso")

# inicia aplicação
if __name__ == "__main__":
    menu_principal()
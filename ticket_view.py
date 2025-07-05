from ticket_controller import autenticar_usuario, inserir_ticket, listar_tickets, atender_ticket
from ticket_models import HardwareTicket, SoftwareTicket

def menu():
    print("===== Ticket2Help =====")
    while True:
        username = input("Username: ")
        password = input("Password: ")
        usuario = autenticar_usuario(username, password)
        if usuario:
            print(f"Bem-vindo, {usuario.username}! ({usuario.tipo})")
            break
        else:
            print("Login inválido. Tente novamente.")

    while True:
        print("\n1 - Criar ticket")
        print("2 - Listar tickets")
        if usuario.tipo == 'tecnico':
            print("3 - Atender ticket")
            print("4 - Sair")
        else:
            print("3 - Sair")
        opcao = input("Escolha: ")

        if opcao == '1':
            tipo = input("Tipo (H = Hardware / S = Software): ").upper()
            if tipo == 'H':
                equipamento = input("Equipamento: ")
                avaria = input("Avaria: ")
                ticket = HardwareTicket(str(usuario.usuario_id), equipamento, avaria)
            elif tipo == 'S':
                software = input("Software: ")
                descricao_necessidade = input("Descrição da necessidade: ")
                ticket = SoftwareTicket(str(usuario.usuario_id), software, descricao_necessidade)
            else:
                print("Tipo inválido.")
                continue
            inserir_ticket(ticket)
            print("Ticket criado e salvo no banco de dados.")

        elif opcao == '2':
            listar_tickets()

        elif opcao == '3' and usuario.tipo == 'tecnico':
            atender_ticket()

        elif (opcao == '3' and usuario.tipo != 'tecnico') or (opcao == '4' and usuario.tipo == 'tecnico'):
            break
        else:
            print("Opção inválida.")

if __name__ == '__main__':
    menu()
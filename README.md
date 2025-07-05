# Ticket2Help

[Repositório no GitHub](https://github.com/ducline/Exame-Pratico)

Ticket2Help é uma aplicação de consola para gestão de tickets de helpdesk, desenvolvida em Python com SQL Server, organizada segundo o padrão **MVC** (Model-View-Controller).

## Funcionalidades

- **Login seguro** com username e password (hash SHA-256).
- **Gestão de utilizadores:** técnico e colaborador.
- **Criação de tickets** de hardware e software.
- **Listagem de tickets** com detalhes.
- **Atendimento de tickets** (apenas técnicos), com registo de intervenção.
- **Estados de ticket:** porAtender, atendido, não atendido, em espera.
- **Documentação automática** com Sphinx (ver pasta `docs`).

## Estrutura do Projeto

- `ticket_models.py` — Classes de domínio (Ticket, HardwareTicket, SoftwareTicket, Usuario).
- `ticket_controller.py` — Lógica de negócio e acesso à base de dados.
- `ticket_view.py` — Interface de consola (menus e interação com o utilizador).
- `criar_usuarios.py` — Script para criar utilizadores iniciais.
- `docs/` — Documentação automática Sphinx.

## Estrutura da Base de Dados

```sql
CREATE TABLE Usuario (
    UsuarioID INT IDENTITY PRIMARY KEY,
    Username NVARCHAR(50) NOT NULL UNIQUE,
    PasswordHash NVARCHAR(255) NOT NULL,
    Tipo NVARCHAR(20) NOT NULL -- 'tecnico' ou 'colaborador'
);

CREATE TABLE Ticket (
    TicketID uniqueidentifier NOT NULL DEFAULT NEWSEQUENTIALID() PRIMARY KEY,
    CodigoColaborador NVARCHAR(50) NOT NULL,
    Tipo NVARCHAR(20) NOT NULL,
    DataHoraCriacao DATETIME NOT NULL DEFAULT GETDATE(),
    Estado NVARCHAR(20) NOT NULL
);

CREATE TABLE HardwareTicket (
    TicketID uniqueidentifier NOT NULL PRIMARY KEY,
    Equipamento NVARCHAR(100) NOT NULL,
    Avaria NVARCHAR(255) NOT NULL,
    DataHoraAtendimento DATETIME NULL,
    DescricaoReparacao NVARCHAR(255) NULL,
    Pecas NVARCHAR(255) NULL,
    EstadoAtendimento NVARCHAR(20) NOT NULL
);

CREATE TABLE SoftwareTicket (
    TicketID uniqueidentifier NOT NULL PRIMARY KEY,
    Software NVARCHAR(100) NOT NULL,
    DescricaoNecessidade NVARCHAR(255) NOT NULL,
    DataHoraAtendimento DATETIME NULL,
    DescricaoIntervencao NVARCHAR(255) NULL,
    EstadoAtendimento NVARCHAR(20) NOT NULL
);
```

## Como usar

1. **Instale as dependências:**
   ```
   pip install pyodbc
   ```

2. **Configure a string de conexão** em `ticket_controller.py` para o seu SQL Server.

3. **Crie a base de dados e as tabelas** usando os comandos acima.

4. **Crie utilizadores iniciais**:
   ```bash
   python criar_usuarios.py
   ```

5. **Execute a aplicação:**
   ```bash
   python ticket_view.py
   ```

6. **Documentação automática:**  
   Para gerar a documentação com Sphinx, veja a pasta `docs` e siga os comandos padrão do Sphinx.

## Notas

- Apenas técnicos podem atender tickets.
- O código de colaborador é automaticamente associado ao utilizador autenticado.
- As passwords são guardadas como hash SHA-256 (para produção, recomenda-se bcrypt).
- O projeto segue boas práticas de POO e está organizado em MVC.

---

**Desenvolvido para fins académicos por Daniel Moraes (2022181)**
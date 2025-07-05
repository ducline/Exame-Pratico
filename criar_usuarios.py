import pyodbc
import hashlib

CONN_STR = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=HP_LAPTOP_DAN\\SQLEXPRESS;"
    "DATABASE=db_ticket2help;"
    "UID=user_ticket;"
    "PWD=user_ticket;"
    "TrustServerCertificate=Yes;"
    "Encrypt=No;"
)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def criar_usuarios():
    conn = pyodbc.connect(CONN_STR)
    cursor = conn.cursor()
    # Cria técnico
    cursor.execute(
        "INSERT INTO Usuario (Username, PasswordHash, Tipo) VALUES (?, ?, ?)",
        'tecnico1', hash_password('tecnico1'), 'tecnico'
    )
    # Cria colaborador
    cursor.execute(
        "INSERT INTO Usuario (Username, PasswordHash, Tipo) VALUES (?, ?, ?)",
        'colaborador1', hash_password('colaborador1'), 'colaborador'
    )
    conn.commit()
    conn.close()
    print("Utilizadores criados com sucesso.")

if __name__ == '__main__':
    criar_usuarios()
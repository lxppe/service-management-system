import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "dados.db")

def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT UNIQUE NOT NULL,
            email TEXT,
            observacoes TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            data TEXT NOT NULL,
            prioridade TEXT NOT NULL,
            status TEXT NOT NULL,
            responsavel TEXT,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        )
    """)

    conn.commit()
    conn.close()



def cadastrar_cliente_e_os(
    nome, telefone, email, observacoes,
    descricao, data, prioridade, status, responsavel
):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Verifica se cliente já existe
    cursor.execute("SELECT id FROM clientes WHERE telefone = ?", (telefone,))
    cliente = cursor.fetchone()

    if cliente:
        cliente_id = cliente[0]
    else:
        cursor.execute("""
            INSERT INTO clientes (nome, telefone, email, observacoes)
            VALUES (?, ?, ?, ?)
        """, (nome, telefone, email, observacoes))
        cliente_id = cursor.lastrowid

    # Cria ordem de serviço
    cursor.execute("""
        INSERT INTO ordens_servico
        (cliente_id, descricao, data, prioridade, status, responsavel)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (cliente_id, descricao, data, prioridade, status, responsavel))

    conn.commit()
    conn.close()
    return True



def listar_os():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            ordens_servico.id,
            clientes.nome,
            ordens_servico.status
        FROM ordens_servico
        JOIN clientes ON clientes.id = ordens_servico.cliente_id
        ORDER BY ordens_servico.id DESC
    """)

    dados = cursor.fetchall()
    conn.close()
    return dados



def buscar_detalhes_os(os_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            clientes.nome,
            clientes.telefone,
            clientes.email,
            clientes.observacoes,
            ordens_servico.descricao,
            ordens_servico.data,
            ordens_servico.prioridade,
            ordens_servico.status,
            ordens_servico.responsavel
        FROM ordens_servico
        JOIN clientes ON clientes.id = ordens_servico.cliente_id
        WHERE ordens_servico.id = ?
    """, (os_id,))

    dados = cursor.fetchone()
    conn.close()
    return dados

def listar_clientes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            nome,
            telefone,
            email,
            observacoes
        FROM clientes
        ORDER BY id DESC                   
""", )
    
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_aberto():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM ordens_servico WHERE status='Aberto'")
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_andamento():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM ordens_servico WHERE status='Em andamento'")
    dados = cursor.fetchall()
    conn.close()
    return dados

def buscar_concluido():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT status FROM ordens_servico WHERE status='Concluido'")
    dados = cursor.fetchall()
    conn.close()
    return dados

def listar_ordens_do_cliente(cliente_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            descricao,
            data,
            prioridade,
            status,
            responsavel
        FROM ordens_servico
        WHERE cliente_id = ?
        ORDER BY id DESC
    """, (cliente_id,))

    dados = cursor.fetchall()
    conn.close()
    
def atualizar_status_os(os_id, novo_status):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE ordens_servico
        SET status = ?
        WHERE id = ?
    """, (novo_status, os_id))

    conn.commit()
    conn.close()


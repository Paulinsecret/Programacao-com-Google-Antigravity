from database import obter_conexao

def criar_cliente(nome, email, telefone):
    """Cria um novo cliente no banco de dados."""
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
            (nome, email, telefone)
        )
        conn.commit()
        # Retorna o ID do cliente criado
        return cursor.lastrowid
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def listar_clientes():
    """Retorna a lista de todos os clientes."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone FROM clientes")
    rows = cursor.fetchall()
    conn.close()
    # Converte sqlite3.Row para dicionários comuns
    return [dict(row) for row in rows]

def buscar_cliente(cliente_id):
    """Busca um cliente pelo ID. Retorna None se não for encontrado."""
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, email, telefone FROM clientes WHERE id = ?", (cliente_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None

def atualizar_cliente(cliente_id, nome, email, telefone):
    """Atualiza as informações de um cliente pelo ID. Retorna True se atualizado."""
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "UPDATE clientes SET nome = ?, email = ?, telefone = ? WHERE id = ?",
            (nome, email, telefone, cliente_id)
        )
        conn.commit()
        # Verifica se alguma linha foi de fato alterada
        atualizado = cursor.rowcount > 0
        return atualizado
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def deletar_cliente(cliente_id):
    """Deleta um cliente pelo ID. Retorna True se deletado."""
    conn = obter_conexao()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
        conn.commit()
        deletado = cursor.rowcount > 0
        return deletado
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

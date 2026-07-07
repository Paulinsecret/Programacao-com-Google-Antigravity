from flask import Flask, request, jsonify
from database import inicializar_banco
import models
import sqlite3

app = Flask(__name__)

# Inicializa o banco de dados antes de iniciar o servidor
inicializar_banco()

@app.route('/clientes', methods=['POST'])
def rota_criar_cliente():
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({'erro': 'Nome e email são obrigatórios'}), 400

    nome = dados['nome']
    email = dados['email']
    telefone = dados.get('telefone')

    try:
        novo_id = models.criar_cliente(nome, email, telefone)
        return jsonify({'id': novo_id, 'nome': nome, 'email': email, 'telefone': telefone}), 211
    except sqlite3.IntegrityError:
        return jsonify({'erro': 'O email informado já está cadastrado'}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/clientes', methods=['GET'])
def rota_listar_clientes():
    try:
        clientes = models.listar_clientes()
        return jsonify(clientes), 200
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/clientes/<int:id>', methods=['GET'])
def rota_buscar_cliente(id):
    try:
        cliente = models.buscar_cliente(id)
        if not cliente:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        return jsonify(cliente), 200
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/clientes/<int:id>', methods=['PUT'])
def rota_atualizar_cliente(id):
    dados = request.get_json()
    if not dados or 'nome' not in dados or 'email' not in dados:
        return jsonify({'erro': 'Nome e email são obrigatórios'}), 400

    nome = dados['nome']
    email = dados['email']
    telefone = dados.get('telefone')

    try:
        atualizado = models.atualizar_cliente(id, nome, email, telefone)
        if not atualizado:
            return jsonify({'erro': 'Cliente não encontrado para atualização'}), 404
        return jsonify({'id': id, 'nome': nome, 'email': email, 'telefone': telefone}), 200
    except sqlite3.IntegrityError:
        return jsonify({'erro': 'O email informado já está em uso por outro cliente'}), 400
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

@app.route('/clientes/<int:id>', methods=['DELETE'])
def rota_deletar_cliente(id):
    try:
        deletado = models.deletar_cliente(id)
        if not deletado:
            return jsonify({'erro': 'Cliente não encontrado'}), 404
        return jsonify({'mensagem': 'Cliente deletado com sucesso'}), 200
    except Exception as e:
        return jsonify({'erro': f'Erro interno: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)

import random
import string
import secrets
import sys

# =====================================================================
# ABORDAGEM 1: DESENVOLVEDOR JÚNIOR
# =====================================================================
# Características do código Júnior:
# - Funciona para o propósito básico.
# - Usa 'random' em vez de 'secrets' (menos seguro para criptografia/senhas).
# - Variáveis menos dinâmicas (strings hardcoded).
# - Tratamento de erros feito com 'if' simples e verificação de string (.isnumeric()).
# - Mistura a lógica de interação (print/input) com a lógica de geração na mesma função.
def gerador_junior():
    print("\n[--- MODO JÚNIOR ---]")
    tamanho = input("Qual o tamanho da senha? ")
    
    if not tamanho.isnumeric():
        print("Erro: você precisa digitar um número!")
        return
        
    tamanho_int = int(tamanho)
    if tamanho_int < 8:
        print("Erro: a senha tem que ter pelo menos 8 caracteres.")
        return
        
    letras = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    simbolos = "!@#$%^&*()?"
    tudo = letras + numeros + simbolos
    
    senha = ""
    for i in range(tamanho_int):
        # Apenas pega caracteres aleatórios, não garante que terá de todos os tipos
        senha += random.choice(tudo)
        
    print(f"Senha do Junior: {senha}")


# =====================================================================
# ABORDAGEM 2: DESENVOLVEDOR PLENO
# =====================================================================
# Características do código Pleno:
# - Separação de responsabilidades: uma função gera a senha, outra cuida da interface.
# - Uso adequado de bibliotecas built-in ('string' e 'secrets' para segurança).
# - Uso de try/except para capturar erros de conversão (ValueError).
# - Lógica que garante pelo menos um caractere de cada grupo (maiúscula, minúscula, etc).
def gerar_senha_pleno(tamanho):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    
    # Garantindo variedade
    senha = [
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation)
    ]
    
    # Completando o resto
    for _ in range(tamanho - 4):
        senha.append(secrets.choice(caracteres))
        
    # Mistura final
    secrets.SystemRandom().shuffle(senha)
    return "".join(senha)

def execucao_pleno():
    print("\n[--- MODO PLENO ---]")
    try:
        tamanho = int(input("Informe o tamanho da senha (mínimo 8): "))
        if tamanho < 8:
            print("Tamanho inválido. A senha deve ter no mínimo 8 caracteres.")
            return
            
        senha = gerar_senha_pleno(tamanho)
        print(f"Senha do Pleno: {senha}")
    except ValueError:
        print("Erro: Entrada inválida. Por favor, digite um número inteiro.")


# =====================================================================
# ABORDAGEM 3: DESENVOLVEDOR SÊNIOR
# =====================================================================
# Características do código Sênior:
# - Uso de Orientação a Objetos (Classes) para modularização.
# - Tipagem estática com Type Hints (int, str) para melhor previsibilidade.
# - Criação de Exceções Customizadas que expressam regras de negócio.
# - Docstrings (comentários padrão para documentação).
# - Código extremamente escalável, limpo e testável de forma unitária.

class PasswordLengthError(ValueError):
    """Exceção customizada disparada quando o tamanho da senha é inferior ao permitido."""
    pass

class GeradorSenhaSenior:
    """
    Classe responsável pela lógica de geração de senhas criptograficamente seguras.
    Independente de como os dados são inseridos pelo usuário.
    """
    MIN_LENGTH: int = 8

    @classmethod
    def generate(cls, length: int) -> str:
        """
        Gera uma senha segura contendo caracteres de múltiplas categorias.
        
        Args:
            length (int): O comprimento desejado da senha.
            
        Returns:
            str: A senha embaralhada gerada de forma segura.
            
        Raises:
            PasswordLengthError: Se o comprimento for menor que o mínimo estipulado.
        """
        if length < cls.MIN_LENGTH:
            raise PasswordLengthError(f"O tamanho mínimo exigido é de {cls.MIN_LENGTH} caracteres.")

        # Dicionário organizando os pools de caracteres
        pool = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'symbols': string.punctuation
        }
        
        # Garante a complexidade mínima extraindo um de cada grupo
        password_chars = [secrets.choice(chars) for chars in pool.values()]
        
        # Completa o tamanho restante
        all_chars = "".join(pool.values())
        password_chars.extend(secrets.choice(all_chars) for _ in range(length - len(password_chars)))
        
        # Embaralhamento usando algoritmo seguro, evitando SystemRandom.shuffle direto 
        # para evitar problemas de compatibilidade e otimização
        senha_final = []
        while password_chars:
            char = secrets.choice(password_chars)
            password_chars.remove(char)
            senha_final.append(char)
            
        return "".join(senha_final)

def execucao_senior() -> None:
    print("\n[--- MODO SÊNIOR ---]")
    try:
        entrada = input("Digite o tamanho da senha desejada (>= 8): ")
        tamanho = int(entrada)
        
        # Chamada da regra de negócios encapsulada
        senha_segura = GeradorSenhaSenior.generate(tamanho)
        print(f"Senha do Sênior gerada com sucesso: {senha_segura}")
        
    except PasswordLengthError as pe:
        print(f"[ERRO DE NEGÓCIO] {pe}")
    except ValueError:
        print("[ERRO DE TIPO] A entrada fornecida não é um número inteiro válido.")
    except Exception as e:
        print(f"[ERRO CRÍTICO] Falha inesperada no sistema: {e}")


# =====================================================================
# MENU PRINCIPAL (Controle de Execução)
# =====================================================================
def main():
    while True:
        print("\n" + "=" * 50)
        print("  COMPARATIVO DE GERADORES DE SENHA POR NÍVEL")
        print("=" * 50)
        print("1 - Modo Júnior (Básico, tudo junto, menos seguro)")
        print("2 - Modo Pleno  (Organizado em funções, try/except)")
        print("3 - Modo Sênior (Orientação a objetos, Tipagem, Custom Exceptions)")
        print("0 - Sair do programa")
        
        escolha = input("\nEscolha qual nível de desenvolvedor você quer testar (0-3): ")
        
        if escolha == '1':
            gerador_junior()
        elif escolha == '2':
            execucao_pleno()
        elif escolha == '3':
            execucao_senior()
        elif escolha == '0':
            print("Encerrando o programa. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()

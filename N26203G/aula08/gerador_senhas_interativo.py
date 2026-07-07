import secrets
import string
import sys

def gerar_senha(tamanho: int) -> str:
    """
    Gera uma senha aleatória criptograficamente segura.

    A senha gerada terá o tamanho especificado e conterá obrigatoriamente
    pelo menos um caractere de cada um dos seguintes grupos:
    - Letras minúsculas
    - Letras maiúsculas
    - Dígitos numéricos
    - Caracteres especiais (símbolos)

    Args:
        tamanho (int): O número de caracteres desejado para a senha. Deve ser >= 8.

    Returns:
        str: A senha gerada de forma segura e com os caracteres embaralhados.

    Raises:
        ValueError: Se o tamanho especificado for menor que 8.
    """
    if tamanho < 8:
        raise ValueError("O tamanho mínimo da senha deve ser de 8 caracteres.")

    # Definindo os grupos de caracteres a serem utilizados
    letras_minusculas = string.ascii_lowercase
    letras_maiusculas = string.ascii_uppercase
    digitos = string.digits
    simbolos = string.punctuation  # Ex: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    
    todos_caracteres = letras_minusculas + letras_maiusculas + digitos + simbolos
    
    # Seleção obrigatória de pelo menos um caractere de cada grupo
    # para garantir a complexidade mínima da senha
    senha_parcial = [
        secrets.choice(letras_minusculas),
        secrets.choice(letras_maiusculas),
        secrets.choice(digitos),
        secrets.choice(simbolos)
    ]
    
    # Preenche o restante dos caracteres necessários para atingir o tamanho desejado
    for _ in range(tamanho - len(senha_parcial)):
        senha_parcial.append(secrets.choice(todos_caracteres))
    
    # Embaralha os caracteres da senha_parcial para garantir que as posições 
    # dos caracteres obrigatórios não sejam previsíveis
    senha_embaralhada = []
    while senha_parcial:
        caractere = secrets.choice(senha_parcial)
        senha_parcial.remove(caractere)
        senha_embaralhada.append(caractere)
        
    return "".join(senha_embaralhada)

def main() -> None:
    """
    Função principal que coordena a interação com o usuário,
    obtenção do tamanho da senha e tratamento de erros de entrada.
    """
    print("=" * 50)
    print("      GERADOR DE SENHAS FORTES INTERATIVO")
    print("=" * 50)
    print("Por motivos de segurança, a senha deve ter pelo menos 8 caracteres.\n")

    # Tratamento de exceções para capturar entradas inválidas do usuário
    try:
        entrada_usuario = input("Digite o tamanho desejado para a senha: ")
        tamanho_desejado = int(entrada_usuario)
        
        # Validação da regra de negócio (mínimo de 8 caracteres)
        if tamanho_desejado < 8:
            print("\n[ERRO] O tamanho da senha não pode ser inferior a 8 caracteres.")
            sys.exit(1)
            
        # Geração da senha com o tamanho validado
        senha_gerada = gerar_senha(tamanho_desejado)
        
        print("\n" + "=" * 50)
        print(f"Sua nova senha de {tamanho_desejado} caracteres é: {senha_gerada}")
        print("=" * 50)
        
    except ValueError:
        # Captura o erro caso o usuário digite texto, letras ou símbolos no lugar de um número inteiro
        print("\n[ERRO] Entrada inválida. Por favor, digite um número inteiro válido (ex: 8, 12, 16).")
        sys.exit(1)
    except KeyboardInterrupt:
        # Captura o erro caso o usuário interrompa o programa (Ctrl+C)
        print("\n\n[AVISO] Operação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        # Captura genérica para outros erros não previstos, auxiliando no debug futuro
        print(f"\n[ERRO FATAL] Ocorreu um erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

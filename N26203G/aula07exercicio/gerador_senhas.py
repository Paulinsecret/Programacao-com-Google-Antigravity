import secrets
import string

def gerar_senha(tamanho=8):
    # Definindo os grupos de caracteres
    leiras_minusculas = string.ascii_lowercase
    letras_maiusculas = string.ascii_uppercase
    digitos = string.digits
    simbolos = string.punctuation  # !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    
    todos_caracteres = leiras_minusculas + letras_maiusculas + digitos + simbolos
    
    # Para garantir a mistura ideal contra força bruta no espaço de 8 caracteres,
    # garantimos que pelo menos um caractere de cada grupo esteja presente.
    senha = [
        secrets.choice(leiras_minusculas),
        secrets.choice(letras_maiusculas),
        secrets.choice(digitos),
        secrets.choice(simbolos)
    ]
    
    # Preenche o restante dos caracteres aleatoriamente
    for _ in range(tamanho - len(senha)):
        senha.append(secrets.choice(todos_caracteres))
    
    # Mistura a lista para que a posição dos caracteres garantidos também seja aleatória
    # Usamos o secrets para escolher posições seguras
    senha_embaralhada = []
    while senha:
        caractere = secrets.choice(senha)
        senha.remove(caractere)
        senha_embaralhada.append(caractere)
        
    return "".join(senha_embaralhada)

if __name__ == "__main__":
    senha_gerada = gerar_senha(8)
    print("=" * 40)
    print(f"Senha Gerada: {senha_gerada}")
    print("=" * 40)
    print("Características de segurança:")
    print("- Tamanho fixo de 8 caracteres.")
    print("- Contém letras maiúsculas, minúsculas, números e caracteres especiais.")
    print("- Gerada usando o módulo 'secrets' (segurança criptográfica do Python).")
    print(f"- Espaço de busca (força bruta): ~94^8 = 6.095.689.385.410.816 combinações possíveis.")
    print("=" * 40)

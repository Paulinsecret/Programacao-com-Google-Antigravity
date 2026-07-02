"""
TERMO CLONE - CLI Version
Este módulo implementa uma versão em linha de comando do jogo 'Termo'.

=============================================================================
TODO / Próximos Passos (Observações para o próximo Engenheiro de Software):
=============================================================================
1. [Dicionário / Fonte de Dados]: Expandir a lista de palavras válidas. 
   Atualmente está hardcoded na variável PALAVRAS. Recomenda-se carregar 
   de um arquivo JSON, TXT ou integrando a uma API externa de dicionário PT-BR.
2. [Acentuação]: Implementar suporte a acentuação. A lógica atual trabalha com 
   palavras sem acento. Seria ideal criar uma função que remove os acentos da 
   entrada do usuário, comparando apenas os caracteres puros, mas exibindo a 
   palavra acentuada se houver acerto.
3. [Interface Gráfica (UI)]: Evoluir para uma interface gráfica (Ex: Tkinter 
   ou PyQt) ou Web (Flask/FastAPI + React). Atualmente o output usa códigos de
   escape ANSI (cores no terminal).
4. [Tamanho Dinâmico]: O jogo hoje é travado no tamanho da palavra sorteada 
   (5 letras). Poderia ser parametrizado (ex: modo 6 letras, modo desafio).
5. [Histórico]: Salvar o progresso do usuário localmente usando um arquivo 
   ou sqlite para controlar sequências de vitórias (streak).
=============================================================================
"""

import datetime
import random
import re
import os

# ==========================================
# CONFIGURAÇÕES E ESTILOS VISUAIS
# ==========================================
# Códigos ANSI para colorir a saída no terminal
VERDE = '\033[92m'
AMARELO = '\033[93m'
CINZA = '\033[90m'
RESET = '\033[0m'

MAX_TENTATIVAS = 5

# Dicionário básico de 5 letras
PALAVRAS = [
    "TERMO", "JUSTO", "MUITO", "TEMPO", "SAGAZ", 
    "NEGRO", "MEXER", "TERRA", "FALAR", "NOBRE", 
    "SENSO", "CAUSA", "SUTIL", "VITAL", "MUNDO",
    "FELIZ", "LUGAR", "IDEIA", "SORTE", "LIVRO"
]

def obter_palavra_do_dia():
    """
    Retorna a palavra do dia.
    Usa a data atual como semente (seed) para o gerador de números aleatórios,
    garantindo que durante 24 horas todos tenham a mesma palavra secreta.
    """
    hoje = datetime.date.today()
    seed = int(hoje.strftime("%Y%m%d"))
    random.seed(seed)
    return random.choice(PALAVRAS).upper()

def validar_entrada(tentativa, tamanho_esperado):
    """
    Valida a entrada do usuário garantindo o tratamento de erros:
    - Retorna None se for inválido, e exibe o motivo.
    - Se for válido, retorna a palavra em CAIXA ALTA (Upper).
    """
    tentativa = tentativa.upper().strip()
    
    if len(tentativa) != tamanho_esperado:
        print(f"[{AMARELO}AVISO{RESET}] A palavra deve ter exatamente {tamanho_esperado} letras.")
        return None
        
    if not re.match(r"^[A-Z]+$", tentativa):
        print(f"[{AMARELO}AVISO{RESET}] Digite apenas letras (sem números, espaços ou caracteres especiais).")
        return None
        
    return tentativa

def avaliar_tentativa(tentativa, palavra_secreta):
    """
    Compara a tentativa do usuário com a palavra secreta e aplica as regras do Termo:
    - Verde: Letra na posição exata.
    - Amarelo: Letra existe na palavra, mas em outra posição.
    - Cinza/Normal: Letra não existe na palavra.
    """
    # Usamos uma lista de caracteres restantes para gerenciar as letras amarelas
    # Isso evita "pintar" de amarelo letras repetidas que já foram consumidas
    letras_restantes = list(palavra_secreta)
    cores = [RESET] * len(tentativa)
    
    # 1ª Passagem: Verificar as letras corretas (VERDES)
    for i in range(len(tentativa)):
        if tentativa[i] == palavra_secreta[i]:
            cores[i] = VERDE
            letras_restantes.remove(tentativa[i])
            
    # 2ª Passagem: Verificar as letras deslocadas (AMARELAS) e inexistentes (CINZA)
    for i in range(len(tentativa)):
        if cores[i] == VERDE:
            continue # Já processado na 1ª passagem
            
        if tentativa[i] in letras_restantes:
            cores[i] = AMARELO
            letras_restantes.remove(tentativa[i])
        else:
            cores[i] = CINZA

    # Monta a string final colorida para o console
    saida = ""
    for i in range(len(tentativa)):
        saida += f"{cores[i]}{tentativa[i]}{RESET} "
        
    return saida.strip()

def jogar():
    """
    Loop principal do jogo.
    """
    # Limpa a tela na inicialização
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("==============================================")
    print("               JOGO TERMO - CLI               ")
    print("==============================================")
    print(f"- Você tem {MAX_TENTATIVAS} tentativas.")
    print(f"- As letras em {VERDE}VERDE{RESET} indicam acerto total.")
    print(f"- As letras em {AMARELO}AMARELO{RESET} indicam posição errada.")
    print("==============================================\n")
    
    palavra_secreta = obter_palavra_do_dia()
    tamanho_palavra = len(palavra_secreta)
    
    tentativas_usadas = 0
    ganhou = False
    
    while tentativas_usadas < MAX_TENTATIVAS:
        entrada_bruta = input(f"Tentativa {tentativas_usadas + 1}/{MAX_TENTATIVAS} -> ")
        tentativa_validada = validar_entrada(entrada_bruta, tamanho_palavra)
        
        # Se a entrada não for válida, a iteração não conta como tentativa perdida
        if not tentativa_validada:
            continue
            
        tentativas_usadas += 1
        
        # Exibe o resultado visual pro jogador
        feedback = avaliar_tentativa(tentativa_validada, palavra_secreta)
        print(f"[{tentativa_validada}]: {feedback}\n")
        
        if tentativa_validada == palavra_secreta:
            ganhou = True
            break
            
    # Avaliação de Fim de Jogo
    print("==============================================")
    if ganhou:
        print(f"🎉 PARABÉNS! Você VENCEU! 🎉")
        print(f"Acertou em {tentativas_usadas} de {MAX_TENTATIVAS} tentativas!")
    else:
        print(f"💀 GAME OVER. Você perdeu! 💀")
        print(f"A palavra do dia era: {VERDE}{palavra_secreta}{RESET}")
    print("==============================================")

if __name__ == "__main__":
    try:
        jogar()
    except KeyboardInterrupt:
        print("\n\nJogo encerrado pelo usuário. Até mais!")

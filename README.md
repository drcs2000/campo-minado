# Campo Minado

Este é um jogo de Campo Minado desenvolvido em Python usando a biblioteca Tkinter para a interface gráfica. O jogo permite ao jogador escolher a dificuldade e fornece uma interface moderna com contadores de bombas e tempo jogado.

## Requisitos

- Python 3.x

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/drcs2000/campo-minado.git
   cd campo-minado

2. Instale as dependêcnias (se houver)
    ```bash
    pip install -r requirements.txt

# Como Jogar

1. Execute o jogo
    ```bash
    python main.py

2. Escolha a dificuldade (Fácil, Médio, Difícil) no menu inicial.

3. Use o botão esquerdo do mouse para revelar células e o botão direito para colocar/remover bandeiras.

4. O objetivo é revelar todas as células que não contêm bombas.

# Estrutura do Projeto

- `main.py`: Ponto de entrada do jogo.
- `game.py`: Lógica principal do jogo.
- `board.py`: Representação do tabuleiro.
- `cell.py`: Representação de uma célula do tabuleiro.

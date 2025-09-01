import random

def print_board(board):
    """Afișează tabla de joc."""
    for row in board:
        print(" | ".join(row))
        print("-" * 5)

def check_winner(board, player):
    """Verifică dacă un jucător a câștigat."""
    # Verifică rânduri
    for row in board:
        if all(cell == player for cell in row):
            return True
    # Verifică coloane
    for col in range(3):
        if all(row[col] == player for row in board):
            return True
    # Verifică diagonale
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    """Verifică dacă jocul este remiză."""
    return all(cell != " " for row in board for cell in row)

def player_move(board):
    """Permite jucătorului să facă o mutare."""
    while True:
        try:
            move = int(input("Introdu numărul poziției (1-9): ")) - 1
            row, col = divmod(move, 3)
            if board[row][col] == " ":
                board[row][col] = "X"
                break
            else:
                print("Poziția este deja ocupată. Încearcă din nou.")
        except (ValueError, IndexError):
            print("Mutare invalidă. Introdu un număr între 1 și 9.")

def ai_move(board):
    """AI-ul face o mutare."""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]
    row, col = random.choice(empty_cells)
    board[row][col] = "O"

def main():
    """Funcția principală a jocului."""
    print("Bun venit la X și 0!")
    print("Pozițiile sunt numerotate de la 1 la 9:")
    print("1 | 2 | 3\n4 | 5 | 6\n7 | 8 | 9")
    
    board = [[" " for _ in range(3)] for _ in range(3)]
    
    while True:
        print_board(board)
        
        # Mutarea jucătorului
        player_move(board)
        if check_winner(board, "X"):
            print_board(board)
            print("Felicitări! Ai câștigat!")
            break
        if is_draw(board):
            print_board(board)
            print("Remiză!")
            break
        
        # Mutarea AI-ului
        ai_move(board)
        if check_winner(board, "O"):
            print_board(board)
            print("AI-ul a câștigat!")
            break
        if is_draw(board):
            print_board(board)
            print("Remiză!")
            break

if __name__ == "__main__":
    main()

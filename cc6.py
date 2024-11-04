import random
from typing import List, Tuple


class CandyCrushGame:
    def __init__(self, size=11, target_score_per_game=10000):
        self.size = size
        self.board = self.initialize_board()
        self.score = 0
        self.swaps = 0

    def initialize_board(self) -> List[List[int]]:
        # Initializează tabla cu valori între 1 și 4, unde fiecare număr reprezintă o culoare
        return [[random.randint(1, 4) for _ in range(self.size)] for _ in range(self.size)]

    def print_board(self):
        for row in self.board:
            print(' '.join(map(str, row)))
        print()

    def detect_formations(self) -> Tuple[List[Tuple[int, int]], int]:
        formations = []
        score_increment = 0

        # Detectează formațiuni orizontale
        for i in range(self.size):
            for j in range(self.size - 2):
                if self.board[i][j] != 0 and abs(self.board[i][j]) == abs(self.board[i][j + 1]) == abs(
                        self.board[i][j + 2]):
                    length = 3
                    while j + length < self.size and self.board[i][j] == self.board[i][j + length]:
                        length += 1
                    for k in range(length):
                        formations.append((i, j + k))
                    if length == 3:
                        score_increment += 5
                    elif length == 4:
                        score_increment += 10
                    elif length >= 5:
                        score_increment += 50
                    j += length - 1

        # Detectează formațiuni verticale
        for j in range(self.size):
            for i in range(self.size - 2):
                if self.board[i][j] != 0 and abs(self.board[i][j]) == abs(self.board[i + 1][j]) == abs(
                        self.board[i + 2][j]):
                    length = 3
                    while i + length < self.size and self.board[i][j] == self.board[i + length][j]:
                        length += 1
                    for k in range(length):
                        formations.append((i + k, j))
                    if length == 3:
                        score_increment += 5
                    elif length == 4:
                        score_increment += 10
                    elif length >= 5:
                        score_increment += 50
                    i += length - 1

        # Marchează formațiunile găsite pentru a fi eliminate
        for (i, j) in formations:
            self.board[i][j] = 0

        return formations, score_increment

    def apply_gravity(self):
        # Aplica gravitatea, făcând ca bomboanele să coboare
        for j in range(self.size):
            empty_row = self.size - 1
            for i in range(self.size - 1, -1, -1):
                if self.board[i][j] > 0:
                    self.board[empty_row][j] = self.board[i][j]
                    if empty_row != i:
                        self.board[i][j] = 0
                    empty_row -= 1

    def refill_board(self):
        # Completează spațiile goale cu bomboane noi
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 0:
                    self.board[i][j] = random.randint(1, 4)

    def find_swaps(self) -> bool:
        n = self.size
        # Caută permutări posibile
        for i in range(n):
            for j in range(n - 1):
                self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
                if self.detect_formations()[0]:
                    self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]
                    self.swaps += 1
                    return True
                self.board[i][j], self.board[i][j + 1] = self.board[i][j + 1], self.board[i][j]

        for j in range(n):
            for i in range(n - 1):
                self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
                if self.detect_formations()[0]:
                    self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]
                    self.swaps += 1
                    return True
                self.board[i][j], self.board[i + 1][j] = self.board[i + 1][j], self.board[i][j]

        return False

    def play_game(self, max_score: int) -> Tuple[int, int]:
        self.score = 0
        self.swaps = 0
        while self.score < max_score:
            formations, score_increment = self.detect_formations()
            if not formations:
                if not self.find_swaps():
                    break
            else:
                self.score += score_increment
                self.apply_gravity()
                self.refill_board()
        # Asigură că scorul jocului nu depășește scorul maxim cerut
        self.score = min(self.score, max_score)
        return self.score, self.swaps


def simulate_games(num_games=100, total_target_score=10000):
    total_score = 0
    total_swaps = 0
    individual_scores = []

    for i in range(num_games):
        game = CandyCrushGame()

        # Verifică dacă mai avem nevoie de puncte pentru a atinge scorul total de 10.000
        remaining_score = total_target_score - total_score
        if remaining_score <= 0:
            break

        # Joacă jocul și asigură că scorul nu depășește ce ne trebuie pentru a ajunge la 10.000
        max_score_for_game = remaining_score // (num_games - i)
        score, swaps = game.play_game(max_score_for_game)

        individual_scores.append(score)
        total_score += score
        total_swaps += swaps
        print(f"Scorul pentru jocul {i + 1}: {score}")  # Afișează scorul pentru fiecare joc

    # Afișează scorul total și media scorurilor și a permutărilor
    print(f"\nScor total al tuturor jocurilor: {total_score}")
    print(f"Media scorurilor: {total_score / num_games}")
    print(f"Media numărului de permutări: {total_swaps / num_games}")


# Rulează simularea pentru 100 de jocuri cu scor total de exact 10.000
simulate_games()

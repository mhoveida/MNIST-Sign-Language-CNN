"""Maddison Hoveida, UNI: mh4572"""

import time
import numpy as np
from BaseAI import BaseAI

(PLAYER_TURN, COMPUTER_TURN) = (0, 1)

class IntelligentAgent(BaseAI):
    def __init__(self):
        self.start_time = None
        self.time_limit = 0.18
    def getMove(self, grid):
            #return the best move by calling expectiminimax function
            self.start_time = time.process_time()
            max_exploring_depth = 1
            best_child = None

            while True:
                try:
                    child, _ = self.expectiminimax(grid=grid, depth=max_exploring_depth, turn=PLAYER_TURN)
                    if child is not None:
                        best_child = child
                    max_exploring_depth += 2
                except TimeoutError:
                    # stop searching when a TimeoutError occurs
                    break

            available_moves = [x for x, g in grid.getAvailableMoves()]
            return best_child if best_child is not None else available_moves[np.random.choice(len(available_moves))]
    

    def expectiminimax(self, grid, depth, alpha= float('-inf'), beta=float('inf'), turn = PLAYER_TURN):
        if time.process_time() - self.start_time >= self.time_limit:
            raise TimeoutError

        if depth == 0 or not grid.canMove():
            return None, self.evaluate(grid)

        if turn == PLAYER_TURN:
            max_utility = float('-inf')
            max_child = None
            for child, child_grid in grid.getAvailableMoves():
                _, utility = self.expectiminimax(grid = child_grid, depth = depth-1, alpha = alpha, beta = beta, turn=COMPUTER_TURN)

                if utility > max_utility:
                    max_utility = utility
                    max_child = child

                if alpha >= beta:
                    break

                if max_utility > alpha:
                    alpha = max_utility

            return max_child, max_utility

        elif turn == COMPUTER_TURN:
            available_cells = grid.getAvailableCells()
            if not available_cells:
                return None, self.evaluate(grid)

            min_utility = float('inf')
            for cell in grid.getAvailableCells():
                # place tile 2
                new_grid = grid.clone()
                new_grid.insertTile(cell, 2)
                _, utility_tile2 = self.expectiminimax(new_grid, depth-1, alpha, beta, turn=PLAYER_TURN)
                utility = 0.9 * utility_tile2

                new_grid = grid.clone()
                new_grid.insertTile(cell, 4)
                _, utility_tile4 = self.expectiminimax(new_grid, depth - 1, alpha, beta, turn=PLAYER_TURN)
                utility += 0.1 * utility_tile4

                if utility < min_utility:
                    min_utility = utility

                if beta <= alpha:
                    break

                if min_utility < beta:
                    beta = min_utility

            return None, min_utility

    def evaluate(self, grid):
        empty_tiles = len(grid.getAvailableCells())/16
        max_tile = grid.getMaxTile()/2048
        monotonicity = self.calculate_monotonicity(grid)
        smoothness = self.calculate_smoothness(grid)
        merge_potential = self.calculate_merge_potential(grid)
        weighted_tile = self.calculate_weighted_tile_sum(grid)

        return (
            empty_tiles +
            max_tile * 75 +
            monotonicity * 7.5 +
            smoothness * 0.75 +
            merge_potential * 1.25 +
            weighted_tile * 100
        )

    def calculate_monotonicity(self, grid):
        score = 0
        tiles_sum = np.sum(grid.map)
        for row in range(4):
            for col in range(3):
                if grid.map[row][col] >= grid.map[row][col + 1]:
                    score += grid.map[row][col]
                if grid.map[col][row] >= grid.map[col + 1][row]:
                    score += grid.map[col][row]
        return score / tiles_sum

    def calculate_smoothness(self, grid):
        score = 0
        for row in range(4):
            for col in range(4):
                if col < 3 and grid.map[row][col] != 0 and grid.map[row][col  + 1] != 0:
                    score -= abs(grid.map[row][col] - grid.map[row][col + 1])
                if row < 3 and grid.map[row][col] != 0 and grid.map[row + 1][col] != 0:
                    score -= abs(grid.map[row][col] - grid.map[row + 1][col])
        return score / np.sum(grid.map)

    def calculate_weighted_tile_sum(self, grid):
        weight_matrix = [
            [32, 16, 8, 4],
            [16, 8, 4, 2],
            [8, 4, 2, 1],
            [4, 2, 1, 0]
        ]

        weights_sum = np.sum(weight_matrix)
        weighted_sum = 0
        tiles_sum = 0
        for row in range(4):
            for col in range(4):
                tile_value = grid.map[row][col]
                weighted_sum += tile_value * weight_matrix[row][col]
                tiles_sum += tile_value

        return weighted_sum / (tiles_sum * weights_sum)

    def calculate_merge_potential(self, grid):
        score = 0
        for row in range(4):
            for col in range(4):
                if col < 3 and grid.map[row][col] == grid.map[row][col + 1]:
                    score += grid.map[row][col]
                if row < 3 and grid.map[row][col] == grid.map[row + 1][col]:
                    score += grid.map[row][col]
        return score/np.sum(grid.map)
from examples.benchmarks import solveSudoku
import time
import copy


# sudoku
def py_solve_sudoku(board):
    empty = find_empty(board)
    if not empty:
        return True
    row, col = empty
    for i in range(1, 10):
        if valid(board, i, (row, col)):
            board[row][col] = i
            if py_solve_sudoku(board):
                return True
            board[row][col] = 0
    return False


def valid(board, num, pos):
    for i in range(len(board[0])):
        if board[pos[0]][i] == num and pos[1] != i:
            return False
    for i in range(len(board)):
        if board[i][pos[1]] == num and pos[0] != i:
            return False
    box_x = pos[1] // 3
    box_y = pos[0] // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


def find_empty(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == 0:
                return (i, j)
    return None


board = [
    [0, 0, 9, 0, 0, 0, 0, 0, 0],
    [6, 4, 0, 0, 0, 0, 0, 0, 8],
    [7, 2, 0, 1, 3, 9, 0, 0, 0],
    [4, 0, 2, 0, 0, 3, 0, 0, 0],
    [0, 0, 0, 6, 7, 1, 0, 0, 0],
    [0, 0, 0, 8, 0, 0, 3, 0, 7],
    [0, 0, 0, 3, 4, 5, 0, 2, 9],
    [8, 0, 0, 0, 0, 0, 0, 1, 3],
    [0, 0, 0, 0, 0, 0, 4, 0, 0],
]
board_flat = [cell for row in board for cell in row]

t0 = time.time()
for _ in range(5):
    solveSudoku(board_flat, False)
t1 = time.time()
for _ in range(5):
    py_solve_sudoku(copy.deepcopy(board))
t2 = time.time()


t_go = t1 - t0
t_py = t2 - t1
print(f"Go is {t_py / t_go:.1f}x faster on sudoku")

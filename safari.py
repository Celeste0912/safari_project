import random
from typing import List, Tuple

EMPTY = '.'
ZEBRA = 'Z'
LION = 'L'

DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def in_bounds(x: int, y: int, rows: int, cols: int) -> bool:
    return 0 <= x < rows and 0 <= y < cols

def display_grid(grid: List[List[str]]) -> None:
    for row in grid:
        print(''.join(row))
    print('-' * len(grid[0]))

def find_move(entity: str, x: int, y: int, grid: List[List[str]]) -> Tuple[int, int]:
    rows, cols = len(grid), len(grid[0])
    possible_moves = []

    if entity == ZEBRA:
        # 얼룩말: 빈칸으로만 이동 가능
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, rows, cols) and grid[nx][ny] == EMPTY:
                possible_moves.append((nx, ny))

    elif entity == LION:
        # 사자: 먼저 얼룩말 찾기
        for dx, dy in DIRECTIONS:
            nx, ny = x + dx, y + dy
            if in_bounds(nx, ny, rows, cols) and grid[nx][ny] == ZEBRA:
                possible_moves.append((nx, ny))
        # 얼룩말 없으면 빈칸 이동
        if not possible_moves:
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if in_bounds(nx, ny, rows, cols) and grid[nx][ny] == EMPTY:
                    possible_moves.append((nx, ny))

    return random.choice(possible_moves) if possible_moves else (x, y)

def simulate(grid: List[List[str]], steps: int) -> None:
    rows, cols = len(grid), len(grid[0])

    for step in range(steps):
        print(f"Step {step + 1}")
        moved = [[False] * cols for _ in range(rows)]
        new_grid = [row.copy() for row in grid]

        # 1단계: 얼룩말 이동
        for x in range(rows):
            for y in range(cols):
                if grid[x][y] == ZEBRA and not moved[x][y]:
                    nx, ny = find_move(ZEBRA, x, y, grid)
                    if (nx, ny) != (x, y):
                        new_grid[nx][ny] = ZEBRA
                        new_grid[x][y] = EMPTY
                        moved[nx][ny] = True

        grid = [row.copy() for row in new_grid]

        # 2단계: 사자 이동
        moved = [[False] * cols for _ in range(rows)]
        for x in range(rows):
            for y in range(cols):
                if grid[x][y] == LION and not moved[x][y]:
                    nx, ny = find_move(LION, x, y, grid)
                    if (nx, ny) != (x, y):
                        new_grid[nx][ny] = LION
                        new_grid[x][y] = EMPTY
                        moved[nx][ny] = True

        grid = new_grid
        display_grid(grid)

# 예시 실행
initial_grid = [
    list("..Z.."),
    list(".ZLZ."),
    list("..Z.."),
    list("..L.."),
    list("....."),
]

simulate(initial_grid, steps=5)
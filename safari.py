import random
import os

# 시뮬레이션 설정
SIZE = 50
ZEBRA_COUNT = 20
LION_COUNT = 5

# 출력 기호
GRASS = '.'
ZEBRA_SYMBOL = 'O'
LION_SYMBOL = 'X'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

class Cell:
    def __init__(self):
        self.has_grass = True
        self.animal = None
        self.grass_regrow_timer = 0

    def step(self):
        if not self.has_grass:
            self.grass_regrow_timer -= 1
            if self.grass_regrow_timer <= 0:
                self.has_grass = True

class Animal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 0
        self.hungry = 0

    def move_to(self, new_x, new_y, world):
        world.grid[self.x][self.y].animal = None
        self.x, self.y = new_x, new_y
        world.grid[self.x][self.y].animal = self

    def possible_moves(self, world):
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        moves = []
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                moves.append((nx, ny))
        random.shuffle(moves)
        return moves

class Zebra(Animal):
    def act(self, world):
        self.age += 1

        # 이동
        for nx, ny in self.possible_moves(world):
            cell = world.grid[nx][ny]
            if cell.animal is None:
                self.move_to(nx, ny, world)
                break

        # 번식 (만 3살 이후부터 매년)
        if self.age >= 4:
            for nx, ny in self.possible_moves(world):
                cell = world.grid[nx][ny]
                if cell.animal is None:
                    baby = Zebra(nx, ny)
                    cell.animal = baby
                    world.new_animals.append(baby)
                    break

class Lion(Animal):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.hungry = 0

    def act(self, world):
        self.age += 1
        self.hungry += 1
        moved = False

        # 사냥
        for nx, ny in self.possible_moves(world):
            cell = world.grid[nx][ny]
            if isinstance(cell.animal, Zebra):
                cell.animal = None
                self.move_to(nx, ny, world)
                self.hungry = 0
                moved = True
                break

        if not moved:
            for nx, ny in self.possible_moves(world):
                cell = world.grid[nx][ny]
                if cell.animal is None:
                    self.move_to(nx, ny, world)
                    break

        # 굶어 죽음
        if self.hungry >= 5:
            world.grid[self.x][self.y].animal = None
            return

        # 번식 (만 5살 이후부터 매년)
        if self.age >= 6:
            for nx, ny in self.possible_moves(world):
                cell = world.grid[nx][ny]
                if cell.animal is None:
                    baby = Lion(nx, ny)
                    cell.animal = baby
                    world.new_animals.append(baby)
                    break

class World:
    def __init__(self):
        self.grid = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]
        self.animals = []
        self.new_animals = []
        self.spawn_animals(Zebra, ZEBRA_COUNT)
        self.spawn_animals(Lion, LION_COUNT)

    def spawn_animals(self, animal_type, count):
        for _ in range(count):
            while True:
                x = random.randint(0, SIZE-1)
                y = random.randint(0, SIZE-1)
                if self.grid[x][y].animal is None:
                    a = animal_type(x, y)
                    self.grid[x][y].animal = a
                    self.animals.append(a)
                    break

    def step(self):
        random.shuffle(self.animals)
        self.new_animals = []

        for row in self.grid:
            for cell in row:
                cell.step()

        for animal in self.animals[:]:
            if self.grid[animal.x][animal.y].animal is animal:
                animal.act(self)

        self.animals = [a for row in self.grid for cell in row if (a := cell.animal)]
        self.animals += self.new_animals

    def display(self):
        # 열 번호 출력
        col_header = '     ' + ' '.join(f'{i:02}' for i in range(SIZE))
        print(col_header)
        print('   +' + '-' * (SIZE * 3) + '+')
        for row_idx, row in enumerate(self.grid):
            line = f'{row_idx:02} |'
            for cell in row:
                if isinstance(cell.animal, Zebra):
                    line += f' {ZEBRA_SYMBOL} '
                elif isinstance(cell.animal, Lion):
                    line += f' {LION_SYMBOL} '
                elif cell.has_grass:
                    line += f' {GRASS} '
            line += '|'
            print(line)
        print('   +' + '-' * (SIZE * 3) + '+')

# 메인 실행부
if __name__ == '__main__':
    world = World()
    year = 1
    while True:
        clear_screen()
        print(f"Year {year}")
        world.display()
        user_input = input("Press Enter to continue, or 'q' to quit: ")
        if user_input.strip().lower() == 'q':
            break
        world.step()
        year += 1

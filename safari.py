import random
import os
from typing import List, Type, Optional

# Simulation settings
SIZE: int = 20
ZEBRA_COUNT: int = 20
LION_COUNT: int = 5
LION_HUNGER_LIMIT: int = 5  # 狮子饥饿上限（步）

# Display symbols
EMPTY_SYMBOL: str = '-'
ZEBRA_SYMBOL: str = 'O'
LION_SYMBOL: str = 'X'


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

class Cell:
    """地图单元格：仅管理动物"""
    def __init__(self) -> None:
        self.animal: Optional[Animal] = None

class Animal:
    """基类：管理位置、年龄、饥饿与行动"""
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.age = 0
        self.hunger = 0  # 仅用于狮子

    def move_to(self, nx: int, ny: int, world: 'World') -> None:
        world.grid[self.x][self.y].animal = None
        self.x, self.y = nx, ny
        world.grid[nx][ny].animal = self

    def possible_moves(self, world: 'World') -> List[tuple]:
        moves = []
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = self.x+dx, self.y+dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                moves.append((nx,ny))
        random.shuffle(moves)
        return moves

    def act(self, world: 'World') -> None:
        raise NotImplementedError

class Zebra(Animal):
    """斑马：移动、繁殖"""
    def act(self, world: 'World') -> None:
        self.age += 1

        # 移动
        for nx, ny in self.possible_moves(world):
            if world.grid[nx][ny].animal is None:
                self.move_to(nx, ny, world)
                break

        # 繁殖：每4步一次
        if self.age % 4 == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    baby = Zebra(nx, ny)
                    world.grid[nx][ny].animal = baby
                    world.new_animals.append(baby)
                    break

class Lion(Animal):
    """狮子：捕食斑马、移动、繁殖、饥饿死亡"""
    def act(self, world: 'World') -> None:
        self.age += 1
        self.hunger += 1

        # 捕食斑马
        hunted = False
        for nx, ny in self.possible_moves(world):
            if isinstance(world.grid[nx][ny].animal, Zebra):
                world.grid[nx][ny].animal = None
                self.move_to(nx, ny, world)
                self.hunger = 0
                hunted = True
                break

        # 未捕食则移动
        if not hunted:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    self.move_to(nx, ny, world)
                    break

        # 饥饿死亡
        if self.hunger >= LION_HUNGER_LIMIT:
            world.grid[self.x][self.y].animal = None
            return

        # 繁殖：每6步一次
        if self.age % 6 == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    baby = Lion(nx, ny)
                    world.grid[nx][ny].animal = baby
                    world.new_animals.append(baby)
                    break

class World:
    """维护整个生态系统的网格和动物列表"""
    def __init__(self) -> None:
        self.grid = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]
        self.animals: List[Animal] = []
        self.new_animals: List[Animal] = []
        self.spawn(Zebra, ZEBRA_COUNT)
        self.spawn(Lion, LION_COUNT)

    def spawn(self, cls: Type[Animal], count: int) -> None:
        for _ in range(count):
            while True:
                x, y = random.randrange(SIZE), random.randrange(SIZE)
                if self.grid[x][y].animal is None:
                    a = cls(x, y)
                    self.grid[x][y].animal = a
                    self.animals.append(a)
                    break

    def step(self) -> None:
        random.shuffle(self.animals)
        self.new_animals = []
        for a in list(self.animals):
            if self.grid[a.x][a.y].animal is a:
                a.act(self)
        self.animals = [c.animal for row in self.grid for c in row if c.animal]
        self.animals.extend(self.new_animals)

    def display(self) -> None:
        # 顶部边框
        print('   +' + '---'*SIZE + '+')
        # 列号行
        print('   | ' + ' '.join(f'{i:02}' for i in range(SIZE)) + ' |')
        # 中间边框
        print('   +' + '---'*SIZE + '+')
        # 内容行
        for i, row in enumerate(self.grid):
            line = f'{i:02} | ' + ' '.join(
                ZEBRA_SYMBOL if isinstance(cell.animal, Zebra)
                else LION_SYMBOL if isinstance(cell.animal, Lion)
                else EMPTY_SYMBOL
                for cell in row
            ) + ' |'
            print(line)
        # 底部边框
        print('   +' + '---'*SIZE + '+')

if __name__ == '__main__':
    world = World()
    year = 0
    while True:
        clear_screen()
        print(f"Year {year}")
        world.display()
        cmd = input("Enter to continue, 'q' to quit: ")
        if cmd.lower().startswith('q'):
            break
        world.step()
        year += 1

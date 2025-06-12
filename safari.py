import random
import os
from typing import List, Type, Optional

# Simulation settings
SIZE: int = 20
ZEBRA_COUNT: int = 20
LION_COUNT: int = 5
ZEBRA_MAX_AGE: int = 20  # 斑马最大存活年数
LION_MAX_AGE: int = 25  # 狮子最大存活年数
LION_HUNGER_LIMIT: int = 5  # 狮子饥饿上限（步）

# Display symbols
EMPTY_SYMBOL: str = '.'
ZEBRA_SYMBOL: str = 'O'
LION_SYMBOL: str = 'X'


def clear_screen() -> None:
    """
    清理终端屏幕
    """
    os.system('cls' if os.name == 'nt' else 'clear')


class Cell:
    """
    地图单元格：管理动物
    """
    def __init__(self) -> None:
        self.animal: Optional[Animal] = None


class Animal:
    """
    基类：管理基础属性与移动规则
    """
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.age = 0
        self.hungry = 0  # 饥饿程度，仅用于狮子

    def move_to(self, new_x: int, new_y: int, world: 'World') -> None:
        world.grid[self.x][self.y].animal = None
        self.x, self.y = new_x, new_y
        world.grid[new_x][new_y].animal = self

    def possible_moves(self, world: 'World') -> List[tuple]:
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        moves = []
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                moves.append((nx, ny))
        random.shuffle(moves)
        return moves

    def act(self, world: 'World') -> None:
        raise NotImplementedError


class Zebra(Animal):
    """斑马：移动、繁殖、基于年龄死亡"""
    def act(self, world: 'World') -> None:
        self.age += 1

        # 年龄死亡
        if self.age >= ZEBRA_MAX_AGE:
            world.grid[self.x][self.y].animal = None
            return

        # 移动
        for nx, ny in self.possible_moves(world):
            if world.grid[nx][ny].animal is None:
                self.move_to(nx, ny, world)
                break

        # 繁殖：年龄大于2岁且每3年一次
        if self.age > 2 and self.age % 3 == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    baby = Zebra(nx, ny)
                    world.grid[nx][ny].animal = baby
                    world.new_animals.append(baby)
                    break


class Lion(Animal):
    """狮子：捕食斑马、移动、繁殖、基于年龄和饥饿的死亡"""
    def act(self, world: 'World') -> None:
        self.age += 1
        self.hungry += 1

        # 年龄死亡
        if self.age >= LION_MAX_AGE:
            world.grid[self.x][self.y].animal = None
            return

        # 饥饿死亡
        if self.hungry >= LION_HUNGER_LIMIT:
            world.grid[self.x][self.y].animal = None
            return

        # 捕食斑马
        hunted = False
        for nx, ny in self.possible_moves(world):
            if isinstance(world.grid[nx][ny].animal, Zebra):
                world.grid[nx][ny].animal = None
                self.move_to(nx, ny, world)
                self.hungry = 0
                hunted = True
                break

        # 随机移动
        if not hunted:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    self.move_to(nx, ny, world)
                    break

        # 繁殖：年龄大于4岁且每5年一次
        if self.age > 4 and self.age % 5 == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    baby = Lion(nx, ny)
                    world.grid[nx][ny].animal = baby
                    world.new_animals.append(baby)
                    break


class World:
    """管理整个生态系统"""
    def __init__(self) -> None:
        self.grid: List[List[Cell]] = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]
        self.animals: List[Animal] = []
        self.new_animals: List[Animal] = []
        self.spawn_animals(Zebra, ZEBRA_COUNT)
        self.spawn_animals(Lion, LION_COUNT)

    def spawn_animals(self, animal_type: Type[Animal], count: int) -> None:
        for _ in range(count):
            while True:
                x = random.randint(0, SIZE - 1)
                y = random.randint(0, SIZE - 1)
                if self.grid[x][y].animal is None:
                    animal = animal_type(x, y)
                    self.grid[x][y].animal = animal
                    self.animals.append(animal)
                    break

    def step(self) -> None:
        random.shuffle(self.animals)
        self.new_animals = []

        for animal in list(self.animals):
            if self.grid[animal.x][animal.y].animal is animal:
                animal.act(self)

        self.animals = [cell.animal for row in self.grid for cell in row if cell.animal]
        self.animals.extend(self.new_animals)

    def display(self) -> None:
        header = '   ' + ' '.join(f'{i:02}' for i in range(SIZE))
        print(header)
        print('  +' + '---'*SIZE + '+')
        for i, row in enumerate(self.grid):
            line = f'{i:02} |'
            for cell in row:
                if isinstance(cell.animal, Zebra):
                    line += f' {ZEBRA_SYMBOL} '
                elif isinstance(cell.animal, Lion):
                    line += f' {LION_SYMBOL} '
                else:
                    line += f' {EMPTY_SYMBOL} '
            line += ' |'
            print(line)
        print('  +' + '---'*SIZE + '+')


if __name__ == '__main__':
    world = World()
    year = 0
    while True:
        clear_screen()
        print(f"Year {year}")
        world.display()
        cmd = input("Enter to continue, 'q' to quit: ")
        if cmd.lower().startswith('q'):
            print("Simulation ended.")
            break
        world.step()
        year += 1
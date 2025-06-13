import random
import os
from typing import List, Type, Optional

SIZE = 50
ZEBRA_COUNT = 100
LION_COUNT = 25
ZEBRA_REPRO_INTERVAL = 3   
LION_REPRO_INTERVAL = 5    
LION_HUNGER_LIMIT = 5      

EMPTY_SYMBOL = '-'
ZEBRA_SYMBOL = 'O'
LION_SYMBOL = 'X'


def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')

class Cell:
    def __init__(self) -> None:
        self.animal: Optional[Animal] = None

class Animal:
    """基类：管理位置与行动"""
    def __init__(self, x: int, y: int) -> None:
        self.x: int = x
        self.y: int = y
        self.age: int = 0
        self.hunger: int = 0  # 仅用于狮子

    def move_to(self, nx: int, ny: int, world: 'World') -> None:
        world.grid[self.x][self.y].animal = None
        self.x, self.y = nx, ny
        world.grid[nx][ny].animal = self

    def possible_moves(self, world: 'World') -> List[tuple]:
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        moves: List[tuple] = []
        for dx, dy in directions:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                moves.append((nx, ny))
        random.shuffle(moves)
        return moves

    def act(self, world: 'World') -> None:
        raise NotImplementedError

class Zebra(Animal):
    """斑马：移动、繁殖"""
    def act(self, world: 'World') -> None:
        self.age += 1

        for nx, ny in self.possible_moves(world):
            if world.grid[nx][ny].animal is None:
              
                self.move_to(nx, ny, world)
                break

        if self.age % ZEBRA_REPRO_INTERVAL == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    baby = Zebra(nx, ny)
                    world.grid[nx][ny].animal = baby
                    world.new_animals.append(baby)
                    break

class Lion(Animal):
    """狮子：捕食斑马、移动、繁殖与饥饿死亡"""
    def act(self, world: 'World') -> None:
        self.age += 1

        hunted: bool = False
        for nx, ny in self.possible_moves(world):
            target = world.grid[nx][ny].animal
            if isinstance(target, Zebra):
                world.grid[nx][ny].animal = None
                self.move_to(nx, ny, world)
                hunted = True
                self.hunger = 0
                break

        if not hunted:
            self.hunger += 1
            if self.hunger >= LION_HUNGER_LIMIT:
                world.grid[self.x][self.y].animal = None
                return
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    self.move_to(nx, ny, world)
                    break

        if self.age % LION_REPRO_INTERVAL == 0:
            for nx, ny in self.possible_moves(world):
                if world.grid[nx][ny].animal is None:
                    cub = Lion(nx, ny)
                    world.grid[nx][ny].animal = cub
                    world.new_animals.append(cub)
                    break

class World:
    """管理生态系统的网格和动物列表"""
    def __init__(self) -> None:
        self.grid: List[List[Cell]] = [[Cell() for _ in range(SIZE)] for _ in range(SIZE)]
        self.animals: List[Animal] = []
        self.new_animals: List[Animal] = []
        self.spawn(Zebra, ZEBRA_COUNT)
        self.spawn(Lion, LION_COUNT)

    def spawn(self, cls: Type[Animal], count: int) -> None:
        for _ in range(count):
            while True:
                x, y = random.randrange(SIZE), random.randrange(SIZE)
                if self.grid[x][y].animal is None:
                    creature = cls(x, y)
                    self.grid[x][y].animal = creature
                    self.animals.append(creature)
                    break

    def step(self) -> None:
        random.shuffle(self.animals)
        self.new_animals = []
        for creature in list(self.animals):
            if self.grid[creature.x][creature.y].animal is creature:
                creature.act(self)
        self.animals = [cell.animal for row in self.grid for cell in row if cell.animal]
        self.animals.extend(self.new_animals)

    def display(self) -> None:
        print('   +' + '---'*SIZE + '+')
        print('   | ' + ' '.join(f'{i:02}' for i in range(SIZE)) + ' |')
        print('   +' + '---'*SIZE + '+')
        for i, row in enumerate(self.grid):
            line = f'{i:02} | ' + ' '.join(
                ZEBRA_SYMBOL if isinstance(cell.animal, Zebra)
                else LION_SYMBOL if isinstance(cell.animal, Lion)
                else EMPTY_SYMBOL
                for cell in row
            ) + ' |'
            print(line)
        print('   +' + '---'*SIZE + '+')

if __name__ == '__main__':
    world = World()
    iteration = 0
    while True:
        clear_screen()
        print(f"Iteration {iteration}")
        world.display()
        cmd = input("Press Enter to continue, or 'q' to quit: ")
        if cmd.lower().startswith('q'):
            break
        world.step()
        iteration += 1

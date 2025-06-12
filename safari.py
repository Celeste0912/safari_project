import random
import time
from typing import List, Tuple, Optional

class Creature:
    """
    생물 객체로, 위치, 나이, 수명을 가짐

    속성:
        id (int): 생물의 고유 ID
        x (float): x 좌표
        y (float): y 좌표
        age (int): 현재 생존한 스텝 수
        lifetime (int): 최대 수명 (스텝 수 기준)
    """
    def __init__(self, id: int, x: float, y: float, lifetime: int) -> None:
        self.id = id
        self.x = x
        self.y = y
        self.age = 0
        self.lifetime = lifetime

    def step(self, bounds: Tuple[float, float]) -> None:
        """
        랜덤 이동 규칙에 따라 위치를 갱신하고 나이를 증가시킴

        매개변수:
            bounds (Tuple[float, float]): 세계의 너비와 높이
        """
        dx = random.uniform(-1, 1)
        dy = random.uniform(-1, 1)
        self.x = max(0, min(bounds[0], self.x + dx))
        self.y = max(0, min(bounds[1], self.y + dy))
        self.age += 1

    def is_dead(self) -> bool:
        """
        생물이 수명을 다했는지 여부를 반환
        """
        return self.age >= self.lifetime

class World:
    """
    세계 환경으로, 모든 생물의 생성, 업데이트, 렌더링을 관리함

    속성:
        width (float): 세계의 너비
        height (float): 세계의 높이
        creatures (List[Creature]): 현재 생물 리스트
        next_id (int): 다음 생물의 ID
    """
    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height
        self.creatures: List[Creature] = []
        self.next_id = 1

    def spawn(self, n: int, lifetime: int = 20) -> None:
        """
        무작위 위치에 n개의 생물을 생성

        매개변수:
            n (int): 생물 수
            lifetime (int): 각 생물의 수명
        """
        for _ in range(n):
            x = random.uniform(0, self.width)
            y = random.uniform(0, self.height)
            self.creatures.append(Creature(self.next_id, x, y, lifetime))
            self.next_id += 1

    def step(self) -> None:
        """
        세계를 한 스텝 진행시킴: 모든 생물을 업데이트하고 죽은 생물은 제거
        """
        for creature in self.creatures:
            creature.step((self.width, self.height))
        self.creatures = [c for c in self.creatures if not c.is_dead()]

    def render(self) -> None:
        """
        현재 모든 생물의 위치를 콘솔에 출력
        """
        print(f"스텝 진행 | 생물 수: {len(self.creatures)}")
        for c in self.creatures:
            print(f"  ID={c.id}, 위치=({c.x:.1f}, {c.y:.1f}), 나이={c.age}")
        print('-' * 40)

if __name__ == '__main__':
    WIDTH, HEIGHT = 50.0, 20.0
    world = World(WIDTH, HEIGHT)
    world.spawn(n=5, lifetime=15)

    STEPS = 30
    INTERVAL = 0.5  # 초
    for step in range(STEPS):
        world.render()
        world.step()
        time.sleep(INTERVAL)

    print("시뮬레이션 종료.")

from enum import Enum           
from typing import List

class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
    YELLOW = "yellow"

class Brick:
    def __init__(self, weight: int, color: Color = Color.BLUE):
        if weight <= 0:
            raise ValueError("Weight must be positive.")
        self.weight = weight
        self.color = color

    def has_color(self, color: Color) -> bool:
        return self.color == color

    def __repr__(self) -> str:
        return f"[{self.color.value}, {self.weight} g]"

    @staticmethod
    def total_weight(bricks: List['Brick'], colors: List[Color]) -> int:
        total = 0
        for brick in bricks:
            if not colors or brick.color in colors:
                total += brick.weight
        return total

class Child:
    def __init__(self, name: str, favorite_color: Color = Color.GREEN, bricks: List[Brick] = None):
        if not name:
            raise ValueError("Name cannot be empty.")
        self.name = name
        self.favorite_color = favorite_color
        self.bricks = bricks if bricks is not None else []

    def pick_up(self, available_bricks: List[Brick], colors: List[Color]) -> List[Brick]:
        remaining_bricks = []
        for brick in available_bricks:
            if brick.has_color(self.favorite_color) or brick.color in colors:
                self.bricks.append(brick)
            else:
                remaining_bricks.append(brick)
        return remaining_bricks

    def is_happy(self) -> bool:
        favorite_count = sum(1 for brick in self.bricks if brick.has_color(self.favorite_color))
        return favorite_count >= len(self.bricks) - favorite_count

    def __repr__(self) -> str:
        status = ", happy" if self.is_happy() else ""
        return f"[{self.name}, {self.favorite_color.value}, {self.bricks}{status}]"

    def exchange(self, other: 'Child') -> int:
        swaps = 0
        self_index, other_index = 0, 0

        while self_index < len(self.bricks) and other_index < len(other.bricks):
            while self_index < len(self.bricks) and self.bricks[self_index].has_color(self.favorite_color):
                self_index += 1
            while other_index < len(other.bricks) and other.bricks[other_index].has_color(other.favorite_color):
                other_index += 1

            if self_index < len(self.bricks) and other_index < len(other.bricks):
                self.bricks[self_index], other.bricks[other_index] = other.bricks[other_index], self.bricks[self_index]
                swaps += 1
                self_index += 1
                other_index += 1

        return swaps

# Örnek kullanım:
brick1 = Brick(5, Color.RED)
brick2 = Brick(10, Color.BLUE)
brick3 = Brick(8, Color.YELLOW)

child1 = Child("Alice", Color.RED, [brick1])
child2 = Child("Bob", Color.BLUE, [brick2, brick3])

print(child1)
print(child2)

# Çocuklar tuğlaları takas ederler
swaps = child1.exchange(child2)
print(f"Takas sayısı: {swaps}")

print(child1)
print(child2)


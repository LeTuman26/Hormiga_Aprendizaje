import tkinter as tk
from typing import Set, Tuple

class Azucar:
    def __init__(self, canvas, cell_size):
        self.canvas = canvas
        self.cell_size = cell_size
        self.sugar_positions: Set[Tuple[int, int]] = set()
        self.sugar_items: dict[Tuple[int, int], int] = {}  # Maps positions to canvas IDs
        self.points = 0
        self.total_sugar = 0

    def add_sugar(self, grid_x: int, grid_y: int):
        position = (grid_x, grid_y)
        if position not in self.sugar_positions:
            self.sugar_positions.add(position)
            self.total_sugar += 1
            item_id = self._draw_sugar(grid_x, grid_y)
            self.sugar_items[position] = item_id

    def remove_sugar(self, grid_x: int, grid_y: int):
        position = (grid_x, grid_y)
        if position in self.sugar_positions:
            self.sugar_positions.remove(position)
            if position in self.sugar_items:
                self.canvas.delete(self.sugar_items[position])
                del self.sugar_items[position]
            self.total_sugar -= 1

    def collect_sugar(self, grid_x: int, grid_y: int) -> bool:
        position = (grid_x, grid_y)
        if position in self.sugar_positions:
            self.remove_sugar(grid_x, grid_y)
            self.points += 10
            return True
        return False

    def _draw_sugar(self, grid_x: int, grid_y: int) -> int:
        x1 = grid_x * self.cell_size
        y1 = grid_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        # Calculate smaller square (80% of cell size)
        margin = self.cell_size * 0.1
        x1 += margin
        y1 += margin
        x2 -= margin
        y2 -= margin

        return self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue')

    def clear_all(self):
        for item_id in self.sugar_items.values():
            self.canvas.delete(item_id)
        self.sugar_positions.clear()
        self.sugar_items.clear()
        self.points = 0
        self.total_sugar = 0

    def reset_for_new_generation(self):
        """Redraw all sugar for a new generation"""
        # Store current positions
        positions = self.sugar_positions.copy()
        # Clear everything
        self.clear_all()
        # Redraw sugar at original positions
        for x, y in positions:
            self.add_sugar(x, y)

    def get_points(self) -> int:
        return self.points

    def get_sugar_positions(self) -> Set[Tuple[int, int]]:
        return self.sugar_positions.copy()

    def get_total_sugar(self) -> int:
        return self.total_sugar
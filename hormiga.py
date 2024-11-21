import tkinter as tk
import random
import time
import threading
from typing import List, Tuple, Optional, Set


class Hormiga:
    def __init__(self, canvas, cell_size, stats_frame):
        self.canvas = canvas
        self.cell_size = cell_size
        self.stats_frame = stats_frame
        self.position: Optional[Tuple[int, int]] = None
        self.ant_id = None
        self.running = False
        self.generation = 1
        self.best_score = 0
        self.current_score = 0
        self.matrix = None
        self.original_matrix = None  # Store the original matrix state
        self.eaten_sugar: Set[Tuple[int, int]] = set()

        # Create labels for stats
        self.gen_label = tk.Label(stats_frame, text="Generacion: 1")
        self.gen_label.pack(side=tk.LEFT, padx=5)
        self.score_label = tk.Label(stats_frame, text="Puntaje: 0")
        self.score_label.pack(side=tk.LEFT, padx=5)
        self.best_label = tk.Label(stats_frame, text="Mejor puntaje: 0")
        self.best_label.pack(side=tk.LEFT, padx=5)

        # Movement delay (in milliseconds)
        self.move_delay = 100

        # Genetic Algorithm parameters
        self.population_size = 50
        self.chromosome_length = 200  # Maximum moves per ant
        self.mutation_rate = 0.1
        self.current_population: List[List[int]] = []
        self.current_ant_index = 0
        self.current_move_index = 0
        self.generation_scores: List[int] = []

    def create_ant(self, grid_x: int, grid_y: int) -> Optional[Tuple[int, int]]:
        if self.position is not None:
            self.remove_ant()

        x1 = grid_x * self.cell_size + self.cell_size * 0.2
        y1 = grid_y * self.cell_size + self.cell_size * 0.2
        x2 = x1 + self.cell_size * 0.6
        y2 = y1 + self.cell_size * 0.6

        self.ant_id = self.canvas.create_oval(x1, y1, x2, y2, fill='green')
        self.position = (grid_x, grid_y)
        return self.position

    def remove_ant(self):
        if self.ant_id is not None:
            self.canvas.delete(self.ant_id)
            self.ant_id = None
            self.position = None

    def set_matrix(self, matrix):
        self.original_matrix = matrix.copy()  # Store original state
        self.matrix = matrix.copy()
        self.eaten_sugar.clear()

    def move_ant(self, direction: int) -> bool:
        if self.position is None:
            return False

        grid_x, grid_y = self.position
        new_x, new_y = grid_x, grid_y

        # 0: up, 1: right, 2: down, 3: left
        if direction == 0 and grid_y > 0:
            new_y -= 1
        elif direction == 1 and grid_x < len(self.matrix[0]) - 1:
            new_x += 1
        elif direction == 2 and grid_y < len(self.matrix) - 1:
            new_y += 1
        elif direction == 3 and grid_x > 0:
            new_x -= 1

        # Check if the new position is valid (not a wall)
        if self.matrix[new_y][new_x] != 1:
            # Calculate movement in pixels
            dx = (new_x - grid_x) * self.cell_size
            dy = (new_y - grid_y) * self.cell_size

            # Animate the movement
            self.canvas.move(self.ant_id, dx, dy)
            self.canvas.update()

            self.position = (new_x, new_y)

            # Check if ant found sugar that hasn't been eaten
            if self.matrix[new_y][new_x] == 2 and (new_x, new_y) not in self.eaten_sugar:
                self.current_score += 10
                self.score_label.config(text=f"Score: {self.current_score}")
                if self.current_score > self.best_score:
                    self.best_score = self.current_score
                    self.best_label.config(text=f"Best Score: {self.best_score}")

                # Mark sugar as eaten
                self.eaten_sugar.add((new_x, new_y))
                # Update matrix to show sugar is gone
                self.matrix[new_y][new_x] = 0
            return True
        return False

    def initialize_population(self):
        self.current_population = []
        self.generation_scores = []
        for _ in range(self.population_size):
            chromosome = [random.randint(0, 3) for _ in range(self.chromosome_length)]
            self.current_population.append(chromosome)
            self.generation_scores.append(0)

    def crossover(self, parent1: List[int], parent2: List[int]) -> List[int]:
        crossover_point = random.randint(0, len(parent1) - 1)
        child = parent1[:crossover_point] + parent2[crossover_point:]
        return child

    def mutate(self, chromosome: List[int]) -> List[int]:
        mutated = chromosome.copy()
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = random.randint(0, 3)
        return mutated

    def create_next_generation(self):
        # Update score for current chromosome
        self.generation_scores[self.current_ant_index] = self.current_score

        # Sort population by fitness scores
        population_with_scores = list(zip(self.current_population, self.generation_scores))
        sorted_population = sorted(population_with_scores, key=lambda x: x[1], reverse=True)

        # Unzip the sorted population
        sorted_chromosomes, _ = zip(*sorted_population)

        # Keep the best 20% of the population
        elite_size = self.population_size // 5
        new_population = list(sorted_chromosomes[:elite_size])

        # Create rest of the population through crossover and mutation
        while len(new_population) < self.population_size:
            parent1 = random.choice(sorted_chromosomes[:self.population_size // 2])
            parent2 = random.choice(sorted_chromosomes[:self.population_size // 2])
            child = self.crossover(parent1, parent2)
            child = self.mutate(child)
            new_population.append(child)

        self.current_population = new_population
        self.generation_scores = [0] * self.population_size
        self.generation += 1
        self.gen_label.config(text=f"Generation: {self.generation}")

        # Reset matrix to original state for new generation
        self.matrix = self.original_matrix.copy()
        self.eaten_sugar.clear()

    def run_simulation(self):
        if not self.current_population:
            self.initialize_population()

        while self.running:
            # Get current ant's chromosome
            chromosome = self.current_population[self.current_ant_index]

            # Execute move
            if self.current_move_index < len(chromosome):
                self.move_ant(chromosome[self.current_move_index])
                self.current_move_index += 1
                time.sleep(self.move_delay / 1000)

            # If ant finished its moves or got stuck
            if self.current_move_index >= len(chromosome):
                # Store score for current chromosome
                self.generation_scores[self.current_ant_index] = self.current_score

                # Move to next ant
                self.current_ant_index += 1
                self.current_move_index = 0

                # Reset ant position and matrix for next ant
                if self.current_ant_index < len(self.current_population):
                    self.reset_ant_position()
                    self.matrix = self.original_matrix.copy()
                    self.eaten_sugar.clear()

                # If generation complete, create next generation
                if self.current_ant_index >= len(self.current_population):
                    self.create_next_generation()
                    self.current_ant_index = 0
                    self.reset_ant_position()

    def reset_ant_position(self):
        if self.position is not None:
            original_x, original_y = self.position
            self.remove_ant()
            self.create_ant(original_x, original_y)
            self.current_score = 0
            self.score_label.config(text=f"Score: {self.current_score}")

    def start_simulation(self):
        if not self.running:
            self.running = True
            self.simulation_thread = threading.Thread(target=self.run_simulation)
            self.simulation_thread.daemon = True
            self.simulation_thread.start()

    def stop_simulation(self):
        self.running = False
        if hasattr(self, 'simulation_thread'):
            self.simulation_thread.join(timeout=1.0)
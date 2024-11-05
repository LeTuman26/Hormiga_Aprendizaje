import tkinter as tk
from tkinter import messagebox
import numpy as np
from hormiga import Hormiga


class LabyrinthCreator:
    def __init__(self, root):
        self.root = root
        self.root.title("Labyrinth Creator")
        self.root.geometry("850x650")


        self.main_frame = tk.Frame(root)
        self.main_frame.pack(expand=True, padx=20, pady=10)


        self.stats_frame = tk.Frame(self.main_frame)
        self.stats_frame.pack(pady=5)


        self.cell_size = 40
        self.grid_size = 10
        self.canvas = tk.Canvas(self.main_frame, width=400, height=400, bg='white')
        self.canvas.pack(pady=5)


        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)


        self.hormiga = Hormiga(self.canvas, self.cell_size, self.stats_frame)


        self.control_panel = tk.Frame(self.main_frame)
        self.control_panel.pack(pady=10)


        self.current_mode = None


        self.walls = set()
        self.azucar = set()
        self.vino = set()
        self.veneno = set()


        self.mode_to_value = {
            'wall': 1,
            'azucar': 2,
            'vino': 3,
            'veneno': 4,
            'ant': 5
        }


        button_width = 15
        button_height = 1

        self.wall_button = tk.Button(
            self.control_panel,
            text="Wall Mode: OFF",
            command=lambda: self.toggle_mode('wall'),
            width=button_width,
            height=button_height
        )
        self.wall_button.pack(side=tk.LEFT, padx=5)

        self.azucar_button = tk.Button(
            self.control_panel,
            text="Azucar Mode: OFF",
            command=lambda: self.toggle_mode('azucar'),
            width=button_width,
            height=button_height
        )
        self.azucar_button.pack(side=tk.LEFT, padx=5)

        self.vino_button = tk.Button(
            self.control_panel,
            text="Vino Mode: OFF",
            command=lambda: self.toggle_mode('vino'),
            width=button_width,
            height=button_height
        )
        self.vino_button.pack(side=tk.LEFT, padx=5)

        self.veneno_button = tk.Button(
            self.control_panel,
            text="Veneno Mode: OFF",
            command=lambda: self.toggle_mode('veneno'),
            width=button_width,
            height=button_height
        )
        self.veneno_button.pack(side=tk.LEFT, padx=5)

        self.ant_button = tk.Button(
            self.control_panel,
            text="Ant Mode: OFF",
            command=lambda: self.toggle_mode('ant'),
            width=button_width,
            height=button_height
        )
        self.ant_button.pack(side=tk.LEFT, padx=5)

        self.reset_button = tk.Button(
            self.control_panel,
            text="Reset All",
            command=self.reset_labyrinth,
            width=button_width,
            height=button_height
        )
        self.reset_button.pack(side=tk.LEFT, padx=5)


        self.print_button = tk.Button(
            self.main_frame,
            text="Print Matrix",
            command=self.print_matrix,
            width=button_width,
            height=button_height
        )
        self.print_button.pack(pady=5)




        self.create_grid()
        self.create_borders()

        self.canvas.bind('<Button-1>', self.handle_click)

    def print_matrix(self):
        print("\nMatriz:")
        print(self.matrix)

    def toggle_mode(self, mode):

        self.wall_button.config(text="Roca/Muro: OFF")
        self.azucar_button.config(text="Azucar: OFF")
        self.vino_button.config(text="Vino: OFF")
        self.veneno_button.config(text="Veneno: OFF")
        self.ant_button.config(text="Hormiga: OFF")

        if self.current_mode == mode:
            self.current_mode = None
        else:
            self.current_mode = mode
            button_text = {
                'wall': 'Roca: ON',
                'azucar': 'Azucar: ON',
                'vino': 'Vino: ON',
                'veneno': 'Veneno: ON',
                'hormiga': 'Hormiga: ON'
            }
            if mode == 'wall':
                self.wall_button.config(text=button_text[mode])
            elif mode == 'azucar':
                self.azucar_button.config(text=button_text[mode])
            elif mode == 'vino':
                self.vino_button.config(text=button_text[mode])
            elif mode == 'veneno':
                self.veneno_button.config(text=button_text[mode])
            elif mode == 'ant':
                self.ant_button.config(text=button_text[mode])

    def create_grid(self):

        for i in range(self.grid_size + 1):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, 400, fill='gray')


        for i in range(self.grid_size + 1):
            y = i * self.cell_size
            self.canvas.create_line(0, y, 400, y, fill='gray')

    def create_borders(self):

        for i in range(self.grid_size):

            self.walls.add((i, 0))
            self.matrix[0][i] = 1
            self.fill_cell(i, 0, 'wall')

            self.walls.add((i, self.grid_size - 1))
            self.matrix[self.grid_size - 1][i] = 1
            self.fill_cell(i, self.grid_size - 1, 'wall')

            self.walls.add((0, i))
            self.matrix[i][0] = 1
            self.fill_cell(0, i, 'wall')

            self.walls.add((self.grid_size - 1, i))
            self.matrix[i][self.grid_size - 1] = 1
            self.fill_cell(self.grid_size - 1, i, 'wall')

    def fill_cell(self, grid_x, grid_y, item_type):
        x1 = grid_x * self.cell_size
        y1 = grid_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        if item_type == 'wall':
            self.canvas.create_rectangle(x1, y1, x2, y2, fill='black')
        elif item_type != 'ant':

            margin = self.cell_size * 0.1
            x1 += margin
            y1 += margin
            x2 -= margin
            y2 -= margin

            colors = {
                'azucar': 'blue',
                'vino': 'red',
                'veneno': 'purple'
            }
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[item_type])

    def clear_cell(self, grid_x, grid_y):
        x1 = grid_x * self.cell_size
        y1 = grid_y * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        self.canvas.create_rectangle(x1, y1, x2, y2, fill='white')

        self.matrix[grid_y][grid_x] = 0

    def handle_click(self, event):
        if not self.current_mode:
            messagebox.showinfo("Off", "Elija algo")
            return


        grid_x = event.x // self.cell_size
        grid_y = event.y // self.cell_size


        if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:

            if grid_x in [0, self.grid_size - 1] or grid_y in [0, self.grid_size - 1]:
                messagebox.showwarning("Error", "No puede")
                return

            if self.current_mode == 'ant':

                if self.matrix[grid_y][grid_x] == 0:
                    self.hormiga.remove_ant()
                    ant_pos = self.hormiga.create_ant(grid_x, grid_y)
                    if ant_pos:
                        self.matrix[grid_y][grid_x] = self.mode_to_value['ant']
                return


            coord = (grid_x, grid_y)
            self.walls.discard(coord)
            self.azucar.discard(coord)
            self.vino.discard(coord)
            self.veneno.discard(coord)


            self.clear_cell(grid_x, grid_y)


            current_set = {
                'wall': self.walls,
                'azucar': self.azucar,
                'vino': self.vino,
                'veneno': self.veneno
            }[self.current_mode]


            if coord not in current_set:
                current_set.add(coord)
                self.fill_cell(grid_x, grid_y, self.current_mode)

                self.matrix[grid_y][grid_x] = self.mode_to_value[self.current_mode]

    def reset_labyrinth(self):

        self.walls.clear()
        self.azucar.clear()
        self.vino.clear()
        self.veneno.clear()
        self.hormiga.remove_ant()

        self.matrix = np.zeros((self.grid_size, self.grid_size), dtype=int)
        self.canvas.delete("all")
        self.create_grid()
        self.create_borders()

        self.current_mode = None
        self.toggle_mode(None)


def main():
    root = tk.Tk()
    app = LabyrinthCreator(root)
    root.mainloop()


if __name__ == "__main__":
    main()

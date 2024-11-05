import tkinter as tk


class Hormiga:
    def __init__(self, canvas, cell_size, stats_frame):
        self.canvas = canvas
        self.cell_size = cell_size
        self.ant_size = cell_size * 0.6
        self.position = None
        self.ant_id = None


        self.health = 100
        self.alcohol = 0
        self.points = 0


        self.stats_frame = stats_frame
        self.setup_stat_displays()

    def setup_stat_displays(self):

        self.health_label = tk.Label(self.stats_frame, text="Vida:", font=("Arial", 10))
        self.health_label.grid(row=0, column=0, padx=5, pady=2)

        self.health_canvas = tk.Canvas(self.stats_frame, width=150, height=15, bg='white')
        self.health_canvas.grid(row=0, column=1, padx=5, pady=2)
        self.health_bar = self.health_canvas.create_rectangle(0, 0, 150, 15, fill='green')

        self.health_value = tk.Label(self.stats_frame, text="100/100", font=("Arial", 10))
        self.health_value.grid(row=0, column=2, padx=5, pady=2)


        self.alcohol_label = tk.Label(self.stats_frame, text="Alcohol:", font=("Arial", 10))
        self.alcohol_label.grid(row=1, column=0, padx=5, pady=2)

        self.alcohol_canvas = tk.Canvas(self.stats_frame, width=150, height=15, bg='white')
        self.alcohol_canvas.grid(row=1, column=1, padx=5, pady=2)
        self.alcohol_bar = self.alcohol_canvas.create_rectangle(0, 0, 0, 15, fill='purple')

        self.alcohol_value = tk.Label(self.stats_frame, text="0/50", font=("Arial", 10))
        self.alcohol_value.grid(row=1, column=2, padx=5, pady=2)


        self.points_label = tk.Label(self.stats_frame, text="Puntos:", font=("Arial", 10))
        self.points_label.grid(row=2, column=0, padx=5, pady=2)

        self.points_value = tk.Label(self.stats_frame, text="0", font=("Arial", 10, "bold"))
        self.points_value.grid(row=2, column=1, columnspan=2, padx=5, pady=2)

    def update_stats_display(self):

        health_width = (self.health / 100) * 150
        self.health_canvas.coords(self.health_bar, 0, 0, health_width, 15)
        self.health_value.config(text=f"{self.health}/100")


        if self.health > 60:
            self.health_canvas.itemconfig(self.health_bar, fill='green')
        elif self.health > 30:
            self.health_canvas.itemconfig(self.health_bar, fill='yellow')
        else:
            self.health_canvas.itemconfig(self.health_bar, fill='red')


        alcohol_width = (self.alcohol / 50) * 150
        self.alcohol_canvas.coords(self.alcohol_bar, 0, 0, alcohol_width, 15)
        self.alcohol_value.config(text=f"{self.alcohol}/50")


        self.points_value.config(text=str(self.points))

    def set_health(self, value):
        self.health = max(0, min(100, value))
        self.update_stats_display()

    def set_alcohol(self, value):
        self.alcohol = max(0, min(50, value))
        self.update_stats_display()

    def add_points(self, value):
        self.points += value
        self.update_stats_display()

    def create_ant(self, grid_x, grid_y):

        if self.ant_id:
            self.canvas.delete(self.ant_id)


        center_x = (grid_x * self.cell_size) + (self.cell_size / 2)
        center_y = (grid_y * self.cell_size) + (self.cell_size / 2)


        half_size = self.ant_size / 2
        points = [
            center_x, center_y - half_size,
            center_x - half_size, center_y + half_size,
            center_x + half_size, center_y + half_size
        ]


        self.ant_id = self.canvas.create_polygon(
            points,
            fill='green',
            outline='darkgreen',
            width=2
        )

        self.position = (grid_x, grid_y)
        self.update_stats_display()
        return self.position

    def remove_ant(self):
        if self.ant_id:
            self.canvas.delete(self.ant_id)
            self.ant_id = None
            self.position = None

            self.health = 100
            self.alcohol = 0
            self.points = 0
            self.update_stats_display()

    def get_position(self):
        return self.position
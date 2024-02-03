#Q-learning Algorithm for State of Agent
#Lyn

import tkinter as tk
import random

class Environment:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.agent_position = (0, 0)
        self.goal_position = (rows - 1, cols - 1)
        self.values = [[random.randint(1, 10) for _ in range(cols)] for _ in range(rows)]
        self.learn_rate = 0.1
        self.discount_factor = 0.9

    def move_agent(self, direction):
        row, col = self.agent_position
        if direction == "up" and row > 0:
            self.agent_position = (row - 1, col)
        elif direction == "down" and row < self.rows - 1:
            self.agent_position = (row + 1, col)
        elif direction == "left" and col > 0:
            self.agent_position = (row, col - 1)
        elif direction == "right" and col < self.cols - 1:
            self.agent_position = (row, col + 1)

    def get_agent_position(self):
        return self.agent_position

    def get_value(self, row, col):
        return self.values[row][col]

    def update_value(self, row, col, new_value):
        self.values[row][col] = new_value

    def get_goal_position(self):
        return self.goal_position

    def is_terminal_state(self, position):
        return position == self.goal_position

    def learn(self):
        row, col = self.agent_position
        current_value = self.get_value(row, col)

        if not self.is_terminal_state(self.agent_position):
            max_neighbor_value = max(
                self.get_value(row - 1, col) if row > 0 else 0,
                self.get_value(row + 1, col) if row < self.rows - 1 else 0,
                self.get_value(row, col - 1) if col > 0 else 0,
                self.get_value(row, col + 1) if col < self.cols - 1 else 0
            )

            new_value = current_value + self.learn_rate * (max_neighbor_value + self.discount_factor * current_value - current_value)
            self.update_value(row, col, new_value)

class Agent:
    def __init__(self, environment):
        self.environment = environment

    def move(self):
        directions = ["up", "down", "left", "right"]
        random_direction = random.choice(directions)
        self.environment.move_agent(random_direction)
        self.environment.learn()

class GUIApp:
    def __init__(self, root, environment, agent):
        self.root = root
        self.environment = environment
        self.agent = agent

        self.canvas = tk.Canvas(root, width=300, height=300, bg="white")
        self.canvas.pack()

        self.draw_environment()
        self.draw_agent()

        self.root.bind("<KeyPress>", self.handle_keypress)

    def draw_environment(self):
        cell_size = 300 / self.environment.rows

        for row in range(self.environment.rows):
            for col in range(self.environment.cols):
                x1 = col * cell_size
                y1 = row * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size
                value = self.environment.get_value(row, col)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")
                self.canvas.create_text((x1 + x2) / 2, (y1 + y2) / 2, text=str(value))

        goal_row, goal_col = self.environment.get_goal_position()
        x1 = goal_col * cell_size
        y1 = goal_row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="green")

    def draw_agent(self):
        row, col = self.environment.get_agent_position()
        cell_size = 300 / self.environment.rows
        x1 = col * cell_size
        y1 = row * cell_size
        x2 = x1 + cell_size
        y2 = y1 + cell_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill="red")

    def handle_keypress(self, event):
        key = event.keysym
        if key in ["Up", "Down", "Left", "Right"]:
            self.agent.move()
            self.draw_agent()

            if self.environment.is_terminal_state(self.environment.get_agent_position()):
                self.root.destroy()
                print("Agent reached the goal state. Learning stops.")

if __name__ == "__main__":
    rows = 5
    cols = 5

    environment = Environment(rows, cols)
    agent = Agent(environment)

    root = tk.Tk()
    app = GUIApp(root, environment, agent)
    root.mainloop()

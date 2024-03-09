import tkinter as tk
import random
import time

class MazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.maze = [[0] * cols for _ in range(rows)]

    def generate_maze(self):
        # Generate random maze
        for i in range(self.rows):
            for j in range(self.cols):
                if random.random() < 0.3:  # Adjust density of walls
                    self.maze[i][j] = 1

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.visited = [[False] * self.cols for _ in range(self.rows)]
        self.path = []

    def dfs(self, row, col, canvas, speed):
        if row < 0 or row >= self.rows or col < 0 or col >= self.cols or self.visited[row][col] or self.maze[row][col]:
            return False

        self.visited[row][col] = True
        self.path.append((row, col))

        canvas.create_rectangle(col * 20, row * 20, (col + 1) * 20, (row + 1) * 20, fill="yellow")
        canvas.update()
        time.sleep(speed)

        if row == self.rows - 1 and col == self.cols - 1:
            return True

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            if self.dfs(row + dr, col + dc, canvas, speed):
                return True

        self.path.pop()
        canvas.create_rectangle(col * 20, row * 20, (col + 1) * 20, (row + 1) * 20, fill="white")
        canvas.update()
        time.sleep(speed)

        return False

class MazeSolverApp:
    def __init__(self, root, rows, cols):
        self.root = root
        self.rows = rows
        self.cols = cols
        self.speed = 0.05

        self.canvas = tk.Canvas(root, width=self.cols * 20, height=self.rows * 20)
        self.canvas.pack()

        self.generate_maze()

    def generate_maze(self):
        maze_generator = MazeGenerator(self.rows, self.cols)
        maze_generator.generate_maze()
        self.maze_solver = MazeSolver(maze_generator.maze)
        self.draw_maze()

    def draw_maze(self):
        self.canvas.delete("all")
        for row in range(self.rows):
            for col in range(self.cols):
                if self.maze_solver.maze[row][col]:
                    self.canvas.create_rectangle(col * 20, row * 20, (col + 1) * 20, (row + 1) * 20, fill="black")

        # Solve maze
        if self.maze_solver.dfs(0, 0, self.canvas, self.speed):
            print("Maze solved!")
            self.draw_path()
        else:
            print("No solution found!")

    def draw_path(self):
        for row, col in self.maze_solver.path:
            self.canvas.create_oval(col * 20 + 5, row * 20 + 5, (col + 1) * 20 - 5, (row + 1) * 20 - 5, fill="green")
            self.canvas.update()
            time.sleep(self.speed)

rows, cols = 20, 20 
root = tk.Tk()
app = MazeSolverApp(root, rows, cols)
root.mainloop()


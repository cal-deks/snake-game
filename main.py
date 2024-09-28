import tkinter as tk
import random
import pygame

# Initialize Pygame mixer for sounds
pygame.mixer.init()
pygame.mixer.music.load("background_music.mp3")
pygame.mixer.music.play(-1)

GAME_OVER_SOUND = pygame.mixer.Sound("game_over.wav")

# Game configuration
GAME_WIDTH = 800
GAME_HEIGHT = 600
SPEED = 100
SPACE_SIZE = 20
INITIAL_SNAKE_LENGTH = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"
OBSTACLE_COLOR = "#808080"

class Snake:
    def __init__(self):
        self.body_size = INITIAL_SNAKE_LENGTH
        self.coordinates = []
        self.squares = []
        for _ in range(INITIAL_SNAKE_LENGTH):
            self.coordinates.append([0, 0])
        for x, y in self.coordinates:
            square = canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
            )
            self.squares.append(square)

class Food:
    def __init__(self):
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        canvas.create_oval(
            x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food"
        )

class Obstacle:
    def __init__(self, num_obstacles):
        self.coordinates = []
        for _ in range(num_obstacles):
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            self.coordinates.append([x, y])
            canvas.create_rectangle(
                x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=OBSTACLE_COLOR
            )

def next_turn(snake, food):
    x, y = snake.coordinates[0]
    if direction == 'up':
        y -= SPACE_SIZE
    elif direction == 'down':
        y += SPACE_SIZE
    elif direction == 'left':
        x -= SPACE_SIZE
    elif direction == 'right':
        x += SPACE_SIZE

    snake.coordinates.insert(0, (x, y))
    square = canvas.create_rectangle(
        x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR
    )
    snake.squares.insert(0, square)

    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score, SPEED
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()
        if score % 5 == 0:
            SPEED = int(SPEED * 0.9)
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

def change_direction(new_direction):
    global direction
    opposite_directions = {'left': 'right', 'right': 'left', 'up': 'down', 'down': 'up'}
    if direction != opposite_directions.get(new_direction):
        direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    if (x, y) in snake.coordinates[1:]:
        return True
    if [x, y] in obstacles.coordinates:
        return True
    return False

def game_over():
    pygame.mixer.music.stop()
    GAME_OVER_SOUND.play()
    canvas.delete(tk.ALL)
    canvas.create_text(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2,
        font=('consolas', 70),
        text="GAME OVER",
        fill="red"
    )
    restart_button = tk.Button(window, text="Restart", command=restart_game)
    canvas.create_window(
        canvas.winfo_width() / 2,
        canvas.winfo_height() / 2 + 100,
        window=restart_button
    )

def restart_game():
    global snake, food, obstacles, score, direction, SPEED
    pygame.mixer.music.play(-1)
    canvas.delete(tk.ALL)
    score = 0
    SPEED = 100
    direction = 'down'
    label.config(text=f"Score: {score}")
    snake = Snake()
    food = Food()
    obstacles = Obstacle(num_obstacles=10)
    next_turn(snake, food)

# Set up the main window
window = tk.Tk()
window.title("Snake Game")
window.resizable(False, False)

score = 0
direction = 'down'

label = tk.Label(window, text=f"Score: {score}", font=('consolas', 40))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

# Center the window on the screen
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
position_x = (screen_width // 2) - (window_width // 2)
position_y = (screen_height // 2) - (window_height // 2)
window.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

snake = Snake()
food = Food()
obstacles = Obstacle(num_obstacles=10)

next_turn(snake, food)

window.mainloop()

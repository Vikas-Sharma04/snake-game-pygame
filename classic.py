import pygame, sys, random
from pygame.math import Vector2

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0): self.head = self.head_left
        elif head_relation == Vector2(-1, 0): self.head = self.head_right
        elif head_relation == Vector2(0, 1): self.head = self.head_up
        elif head_relation == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1): self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1): self.tail = self.tail_down

    def move_snake(self):
        if self.direction == Vector2(0, 0):
            return  # Prevent movement until direction is set

        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        # Wrap around screen edges
        self.body[0].x %= cell_number
        # Prevent snake from moving into the banner area (top row)
        if self.body[0].y < 1:  # If the snake enters the banner area
            self.body[0].y = cell_number - 1  # Move to the bottom
        elif self.body[0].y >= cell_number:  # If the snake goes off the bottom edge
            self.body[0].y = 1  # Move just below the banner


    def add_block(self):
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0) 


class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(1, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self, current_score, speed):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.fruit_count = current_score
        self.speed = speed
        self.game_over_flag = False
        self.paused = False
        self.game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)

    def toggle_pause(self):
        self.paused = not self.paused

    def update(self):
        if not self.paused and not self.game_over_flag:  # Prevent updates when paused or game over
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_banner()
        if self.paused:
            self.draw_pause_message()
        if self.game_over_flag:
            self.draw_game_over_message()

    def draw_pause_message(self):
        pause_text = "Paused. Press P to Resume"
        pause_surface = game_font.render(pause_text, True, (255, 255, 255))
        pause_rect = pause_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(pause_surface, pause_rect)

    def draw_game_over_message(self):
        game_over_text = "Game Over! Press R to Restart"
        game_over_surface = game_font.render(game_over_text, True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(game_over_surface, game_over_rect)

    def game_over(self):
        self.game_over_flag = True

    def reset(self):
        self.snake.reset()
        self.fruit_count = 0
        self.speed = 150
        self.game_over_flag = False
        pygame.time.set_timer(SCREEN_UPDATE, self.speed)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.snake.play_crunch_sound()
            self.fruit_count += 1

            if self.fruit_count % 10 == 0 and self.fruit_count != 0:  # Increase speed every 10 fruits
                self.speed = max(60, self.speed - 8)  # Decrease speed but don't go below a limit
                pygame.time.set_timer(SCREEN_UPDATE, self.speed)

        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over_sound.play()
                self.game_over_flag = True
                self.game_over()

    def draw_banner(self):
        # Gradient colors for the banner
        top_color = (255, 140, 0)  # Orange
        bottom_color = (255, 69, 0)  # Red

        banner_height = 40
        for y in range(banner_height):
            r = top_color[0] + (bottom_color[0] - top_color[0]) * y / banner_height
            g = top_color[1] + (bottom_color[1] - top_color[1]) * y / banner_height
            b = top_color[2] + (bottom_color[2] - top_color[2]) * y / banner_height
            pygame.draw.line(screen, (int(r), int(g), int(b)), (0, y), (cell_size * cell_number, y))

        # Display score and level text
        banner_text = f"Score: {self.fruit_count}"
        banner_surface = game_font.render(banner_text, True, (255, 255, 255))
        banner_rect = banner_surface.get_rect(center=(cell_size * cell_number // 2, 20))
        screen.blit(banner_surface, banner_rect)


def main(current_score=0, speed=150):
    global screen, clock, cell_number, cell_size,apple, game_font,SCREEN_UPDATE
    pygame.mixer.pre_init(44100, -16, 2, 512)
    pygame.init()
    cell_size = 38
    cell_number = 20
    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()
    apple = pygame.image.load('Graphics/apple.png').convert_alpha()
    game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
    pygame.display.set_caption("Snake Game")


    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, 150)

    main_game = MAIN(current_score, speed)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if not main_game.game_over_flag:  # Only allow movement if not game over
                    # Arrow keys and WASD keys for movement
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                    if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                    if (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                    if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_p:  # Toggle pause
                    main_game.toggle_pause()
                if event.key == pygame.K_r and main_game.game_over_flag:  # Restart the game
                    main_game.reset()
                if event.key == pygame.K_x:  # Exit game
                    import main
                    main.main_menu()
                    return
                    
        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        clock.tick(60)

if __name__=='__main__':
    main()
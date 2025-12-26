import pygame, sys, random
import asyncio  # Required for web
from pygame.math import Vector2

class SNAKE:
    def __init__(self, screen_ref, cell_size_ref, cell_number_ref):
        self.screen = screen_ref
        self.cell_size = cell_size_ref
        self.cell_number = cell_number_ref
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Load Graphics
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
            x_pos = int(block.x * self.cell_size)
            y_pos = int(block.y * self.cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, self.cell_size, self.cell_size)

            if index == 0:
                self.screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                self.screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    self.screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    self.screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        self.screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        self.screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        self.screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        self.screen.blit(self.body_br, block_rect)

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
        if self.direction == Vector2(0, 0): return

        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

        # Wrap around screen
        self.body[0].x %= self.cell_number
        if self.body[0].y < 1:
            self.body[0].y = self.cell_number - 1
        elif self.body[0].y >= self.cell_number:
            self.body[0].y = 1

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0) 

class FRUIT:
    def __init__(self, screen_ref, cell_size_ref, cell_number_ref, apple_img):
        self.screen = screen_ref
        self.cell_size = cell_size_ref
        self.cell_number = cell_number_ref
        self.apple = apple_img
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * self.cell_size), int(self.pos.y * self.cell_size), self.cell_size, self.cell_size)
        self.screen.blit(self.apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, self.cell_number - 1)
        self.y = random.randint(1, self.cell_number - 1)
        self.pos = Vector2(self.x, self.y)

class MAIN_GAME:
    def __init__(self, screen, cell_size, cell_number, apple, font, SCREEN_UPDATE, current_score, speed):
        self.screen = screen
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.font = font
        self.SCREEN_UPDATE = SCREEN_UPDATE
        
        self.snake = SNAKE(screen, cell_size, cell_number)
        self.fruit = FRUIT(screen, cell_size, cell_number, apple)
        self.fruit_count = current_score
        self.speed = speed
        self.game_over_flag = False
        self.paused = False
        self.game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
        pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

    def update(self):
        if not self.paused and not self.game_over_flag:
            self.snake.move_snake()
            self.check_collision()
            self.check_fail()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.new_block = True
            self.snake.crunch_sound.play()
            self.fruit_count += 1
            # Progressive difficulty
            if self.fruit_count % 10 == 0 and self.fruit_count != 0:
                self.speed = max(60, self.speed - 8)
                pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

    def check_fail(self):
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over_sound.play()
                self.game_over_flag = True

    def draw_elements(self):
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_banner()
        if self.paused:
            self.draw_message("Paused. Press P to Resume")
        if self.game_over_flag:
            self.draw_message("Game Over! Press R to Restart")

    def draw_message(self, text):
        surf = self.font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(self.cell_size * self.cell_number // 2, self.cell_size * self.cell_number // 2))
        self.screen.blit(surf, rect)

    def draw_banner(self):
        top_color, bottom_color = (255, 140, 0), (255, 69, 0)
        banner_h = 40
        for y in range(banner_h):
            r = top_color[0] + (bottom_color[0] - top_color[0]) * y / banner_h
            g = top_color[1] + (bottom_color[1] - top_color[1]) * y / banner_h
            b = top_color[2] + (bottom_color[2] - top_color[2]) * y / banner_h
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (0, y), (self.cell_size * self.cell_number, y))
        
        surf = self.font.render(f"Score: {self.fruit_count}", True, (255, 255, 255))
        rect = surf.get_rect(center=(self.cell_size * self.cell_number // 2, 20))
        self.screen.blit(surf, rect)

    def reset(self):
        self.snake.reset()
        self.fruit_count = 0
        self.speed = 150
        self.game_over_flag = False
        pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

async def main(current_score=0, speed=150):
    # Initialize basic pygame settings locally for the module
    cell_size, cell_number = 38, 20
    screen = pygame.display.get_surface()
    if screen is None:
        screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    
    clock = pygame.time.Clock()
    apple = pygame.image.load('Graphics/apple.png').convert_alpha()
    game_font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
    
    SCREEN_UPDATE = pygame.USEREVENT
    main_game = MAIN_GAME(screen, cell_size, cell_number, apple, game_font, SCREEN_UPDATE, current_score, speed)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                main_game.update()
            if event.type == pygame.KEYDOWN:
                if not main_game.game_over_flag:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and main_game.snake.direction.y != 1:
                        main_game.snake.direction = Vector2(0, -1)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and main_game.snake.direction.x != -1:
                        main_game.snake.direction = Vector2(1, 0)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and main_game.snake.direction.y != -1:
                        main_game.snake.direction = Vector2(0, 1)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and main_game.snake.direction.x != 1:
                        main_game.snake.direction = Vector2(-1, 0)
                
                if event.key == pygame.K_p:
                    main_game.paused = not main_game.paused
                if event.key == pygame.K_r and main_game.game_over_flag:
                    main_game.reset()
                if event.key == pygame.K_x:
                    return # Exit to main menu

        screen.fill((175, 215, 70))
        main_game.draw_elements()
        pygame.display.update()
        
        await asyncio.sleep(0)
        clock.tick(60)
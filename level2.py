import pygame, sys, random
import asyncio
from pygame.math import Vector2

class SNAKE:
    def __init__(self, screen_ref, cell_size_ref, cell_number_ref):
        self.screen = screen_ref
        self.cell_size = cell_size_ref
        self.cell_number = cell_number_ref
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        # Graphics
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
            if index == 0: self.screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1: self.screen.blit(self.tail, block_rect)
            else:
                prev = self.body[index + 1] - block
                nxt = self.body[index - 1] - block
                if prev.x == nxt.x: self.screen.blit(self.body_vertical, block_rect)
                elif prev.y == nxt.y: self.screen.blit(self.body_horizontal, block_rect)
                else:
                    if prev.x == -1 and nxt.y == -1 or prev.y == -1 and nxt.x == -1: self.screen.blit(self.body_tl, block_rect)
                    elif prev.x == -1 and nxt.y == 1 or prev.y == 1 and nxt.x == -1: self.screen.blit(self.body_bl, block_rect)
                    elif prev.x == 1 and nxt.y == -1 or prev.y == -1 and nxt.x == 1: self.screen.blit(self.body_tr, block_rect)
                    elif prev.x == 1 and nxt.y == 1 or prev.y == 1 and nxt.x == 1: self.screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        rel = self.body[1] - self.body[0]
        if rel == Vector2(1, 0): self.head = self.head_left
        elif rel == Vector2(-1, 0): self.head = self.head_right
        elif rel == Vector2(0, 1): self.head = self.head_up
        elif rel == Vector2(0, -1): self.head = self.head_down

    def update_tail_graphics(self):
        rel = self.body[-2] - self.body[-1]
        if rel == Vector2(1, 0): self.tail = self.tail_left
        elif rel == Vector2(-1, 0): self.tail = self.tail_right
        elif rel == Vector2(0, 1): self.tail = self.tail_up
        elif rel == Vector2(0, -1): self.tail = self.tail_down

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

    def reset(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(0, 0)

class FRUIT:
    def __init__(self, screen, cell_size, cell_number, apple_img, walls):
        self.screen = screen
        self.cell_size = cell_size
        self.cell_number = cell_number
        self.apple = apple_img
        self.walls = walls
        self.randomize()

    def draw_fruit(self):
        rect = pygame.Rect(int(self.pos.x * self.cell_size), int(self.pos.y * self.cell_size), self.cell_size, self.cell_size)
        self.screen.blit(self.apple, rect)

    def randomize(self):
        while True:
            self.pos = Vector2(random.randint(0, self.cell_number - 1), random.randint(1, self.cell_number - 1))
            if self.pos not in self.walls: break

class LEVEL2_MGR:
    def __init__(self, screen, cell_size, cell_number, apple, font, SCREEN_UPDATE, current_score, speed):
        self.screen, self.cell_size, self.cell_number = screen, cell_size, cell_number
        self.font, self.SCREEN_UPDATE = font, SCREEN_UPDATE
        self.wall_rects = self.create_walls()
        self.snake = SNAKE(screen, cell_size, cell_number)
        self.fruit = FRUIT(screen, cell_size, cell_number, apple, self.wall_rects)
        self.fruit_count = current_score
        self.speed = speed
        self.level = 2
        self.game_over_flag = self.level_up_flag = self.paused = False
        self.game_over_sound = pygame.mixer.Sound('Sound/game_over.wav')
        self.level_up_sound = pygame.mixer.Sound('Sound/level_up.wav')
        pygame.time.set_timer(self.SCREEN_UPDATE, self.speed)

    def create_walls(self):
        walls = []
        for x in range(0, self.cell_number):
            walls.append(Vector2(x, 1))
            walls.append(Vector2(x, self.cell_number - 1))
        for y in range(2, self.cell_number - 1):
            walls.append(Vector2(0, y))
            walls.append(Vector2(self.cell_number - 1, y))
        return walls

    def draw_walls(self):
        for wall in self.wall_rects:
            rect = pygame.Rect(int(wall.x * self.cell_size), int(wall.y * self.cell_size), self.cell_size, self.cell_size)
            pygame.draw.rect(self.screen, (0, 0, 0), rect)

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
            if self.fruit_count == 20:
                self.level_up_sound.play()
                self.level_up_flag = True

    def check_fail(self):
        if self.snake.body[0] in self.wall_rects: self.game_over_flag = True
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]: self.game_over_flag = True
        if self.game_over_flag: self.game_over_sound.play()

    def draw_elements(self):
        self.draw_walls()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_banner()
        if self.paused: self.draw_mid_text("Paused. Press P to Resume")
        if self.game_over_flag: self.draw_mid_text("Game Over! Press R to Restart")

    def draw_mid_text(self, text):
        surf = self.font.render(text, True, (255, 255, 255))
        rect = surf.get_rect(center=(self.cell_size * self.cell_number // 2, self.cell_size * self.cell_number // 2))
        self.screen.blit(surf, rect)

    def draw_banner(self):
        top, bottom = (255, 140, 0), (255, 69, 0)
        for y in range(40):
            r = top[0] + (bottom[0] - top[0]) * y / 40
            g = top[1] + (bottom[1] - top[1]) * y / 40
            b = top[2] + (bottom[2] - top[2]) * y / 40
            pygame.draw.line(self.screen, (int(r), int(g), int(b)), (0, y), (self.cell_size * self.cell_number, y))
        surf = self.font.render(f"Score: {self.fruit_count} | Level: {self.level}", True, (255, 255, 255))
        rect = surf.get_rect(center=(self.cell_size * self.cell_number // 2, 20))
        self.screen.blit(surf, rect)

async def main(current_score=0, speed=150):
    pygame.init()
    cs, cn = 38, 20
    screen = pygame.display.set_mode((cn * cs, cn * cs))
    clock, apple_img = pygame.time.Clock(), pygame.image.load('Graphics/apple.png').convert_alpha()
    font = pygame.font.Font('Font/PoetsenOne-Regular.ttf', 25)
    SCREEN_UPDATE = pygame.USEREVENT
    mgr = LEVEL2_MGR(screen, cs, cn, apple_img, font, SCREEN_UPDATE, current_score, speed)

    while True:
        if mgr.level_up_flag:
            import level3
            await level3.main(mgr.fruit_count, max(60, mgr.speed - 10))
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == SCREEN_UPDATE: mgr.update()
            if event.type == pygame.KEYDOWN:
                if not mgr.game_over_flag:
                    if (event.key == pygame.K_UP or event.key == pygame.K_w) and mgr.snake.direction.y != 1: mgr.snake.direction = Vector2(0, -1)
                    elif (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and mgr.snake.direction.x != -1: mgr.snake.direction = Vector2(1, 0)
                    elif (event.key == pygame.K_DOWN or event.key == pygame.K_s) and mgr.snake.direction.y != -1: mgr.snake.direction = Vector2(0, 1)
                    elif (event.key == pygame.K_LEFT or event.key == pygame.K_a) and mgr.snake.direction.x != 1: mgr.snake.direction = Vector2(-1, 0)
                if event.key == pygame.K_p: mgr.paused = not mgr.paused
                if event.key == pygame.K_r and mgr.game_over_flag:
                    import level1
                    await level1.main()
                    return
                if event.key == pygame.K_x: return

        screen.fill((175, 215, 70))
        mgr.draw_elements()
        pygame.display.update()
        await asyncio.sleep(0)
        clock.tick(60)
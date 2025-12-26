import pygame
import sys
import asyncio  # Required for web deployment
import classic  # Assuming classic.py is in the same folder
import level1   # Assuming level1.py is in the same folder

pygame.init()

# Screen dimensions and settings
cell_size = 38
cell_number = 20
screen_width = cell_number * cell_size
screen_height = cell_number * cell_size
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Colors
bg_gradient_top = (190, 0, 0)
bg_gradient_bottom = (255, 69, 0)
button_color = (255, 165, 0)
button_hover_color = (255, 140, 0)
button_shadow_color = (200, 100, 0)
text_color = (255, 255, 255)
name_color = (175, 215, 70)
heading_color = (255, 223, 0)
snake_game_color = (34, 179, 34)

# Fonts
heading_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 50)
instruction_font = pygame.font.Font(None, 30)

# Button settings
button_width = 300
button_height = 60
buttons = ["Classic Game", "Box Game"]
instructions = [
    "Press P to Pause",
    "Press R to Restart when game is over",
    "Press X to Exit to Main Menu",
]

def draw_gradient_background(surface, color_top, color_bottom):
    for y in range(screen_height):
        ratio = y / screen_height
        color = (
            int(color_top[0] + ratio * (color_bottom[0] - color_top[0])),
            int(color_top[1] + ratio * (color_bottom[1] - color_top[1])),
            int(color_top[2] + ratio * (color_bottom[2] - color_top[2])),
        )
        pygame.draw.line(surface, color, (0, y), (screen_width, y))

def draw_text(text, font, color, surface, x, y, center=True):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if center else None)
    if not center:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)

def draw_shadowed_button(x, y, width, height, text, hover, shadow_color, button_color, hover_color, font):
    shadow_offset = 5
    pygame.draw.rect(screen, shadow_color, (x + shadow_offset, y + shadow_offset, width, height), border_radius=15)
    button_actual_color = hover_color if hover else button_color
    pygame.draw.rect(screen, button_actual_color, (x, y, width, height), border_radius=15)
    draw_text(text, font, text_color, screen, x + width // 2, y + height // 2)

async def main():
    """Main menu loop converted for WebAssembly."""
    # Define rectangles for easier collision detection
    button_positions = [
        pygame.Rect((screen_width // 2) - (button_width // 2), (screen_height // 2) + 6, button_width, button_height),
        pygame.Rect((screen_width // 2) - (button_width // 2), (screen_height // 2) + 86, button_width, button_height),
    ]

    while True:
        draw_gradient_background(screen, bg_gradient_top, bg_gradient_bottom)

        snake_game_font = pygame.font.Font(None, 100) 
        draw_text("Snake Game", snake_game_font, snake_game_color, screen, screen_width // 2, 80)

        made_by_font = pygame.font.Font(None, 70)  
        draw_text("Made by Vikas Sharma", made_by_font, name_color, screen, screen_width // 2, 180)

        heading_text = "MAIN MENU"
        main_menu_y_position = screen_height // 4 + 100  
        draw_text(heading_text, heading_font, heading_color, screen, screen_width // 2, main_menu_y_position)
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Draw buttons and handle hover
        for i, rect in enumerate(button_positions):
            hover = rect.collidepoint(mouse_pos)
            draw_shadowed_button(rect.x, rect.y, rect.width, rect.height, buttons[i], hover, button_shadow_color, button_color, button_hover_color, button_font)

        # Instructions UI
        instruction_rect = pygame.Rect((screen_width // 2) - 200, screen_height - 160, 400, 120)
        pygame.draw.rect(screen, text_color, instruction_rect, border_radius=10, width=2) 
        for i, line in enumerate(instructions):
            draw_text(line, instruction_font, text_color, screen, screen_width // 2, screen_height - 130 + (i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Classic Game Logic
                if button_positions[0].collidepoint(mouse_pos):
                    await classic.main()

                # Box (Levels) Game Logic
                if button_positions[1].collidepoint(mouse_pos):
                    await level1.main()

        pygame.display.update()
        
        # This is the secret sauce for Pygbag
        await asyncio.sleep(0) 
        clock.tick(60)

# Entry point for the browser
if __name__ == "__main__":
    asyncio.run(main())
import pygame
import sys

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
bg_gradient_top = (190, 0, 0)  # Red
bg_gradient_bottom = (255, 69, 0)  # Orange-Red
button_color = (255, 165, 0)  # Orange
button_hover_color = (255, 140, 0)  # Darker orange
button_shadow_color = (200, 100, 0)  # Shadow color
text_color = (255, 255, 255)  # White
name_color = (175, 215, 70)
heading_color = (255, 223, 0)  # Yellow
snake_game_color = (34, 179, 34)  # Dark Green

# Fonts
heading_font = pygame.font.Font(None, 80)
button_font = pygame.font.Font(None, 50)
instruction_font = pygame.font.Font(None, 30)

# Button dimensions
button_width = 300
button_height = 60
button_spacing = 20
button_positions = [
    ((screen_width // 2) - (button_width // 2), (screen_height // 2) + 120),  
    ((screen_width // 2) - (button_width // 2), (screen_height // 2) + 200),  
]
buttons = ["Classic Game", "Box Game"]

instructions = [
    "Press P to Pause",
    "Press R to Restart when game is over",
    "Press X to Exit to Main Menu",
]


def draw_gradient_background(surface, color_top, color_bottom):
    """Draw a gradient background."""
    for y in range(screen_height):
        ratio = y / screen_height
        color = (
            int(color_top[0] + ratio * (color_bottom[0] - color_top[0])),
            int(color_top[1] + ratio * (color_bottom[1] - color_top[1])),
            int(color_top[2] + ratio * (color_bottom[2] - color_top[2])),
        )
        pygame.draw.line(surface, color, (0, y), (screen_width, y))


def draw_text(text, font, color, surface, x, y, center=True):
    """Helper function to render text on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y) if center else None)
    if not center:
        text_rect.topleft = (x, y)
    surface.blit(text_surface, text_rect)


def draw_shadowed_button(x, y, width, height, text, hover, shadow_color, button_color, hover_color, font):
    """Draw a button with a shadow."""
    shadow_offset = 5
    pygame.draw.rect(screen, shadow_color, (x + shadow_offset, y + shadow_offset, width, height), border_radius=15)
    button_actual_color = hover_color if hover else button_color
    pygame.draw.rect(screen, button_actual_color, (x, y, width, height), border_radius=15)
    draw_text(text, font, text_color, screen, x + width // 2, y + height // 2)


def main_menu():
    """Main menu loop."""
    while True:
        draw_gradient_background(screen, bg_gradient_top, bg_gradient_bottom)

        snake_game_font = pygame.font.Font(None, 100) 
        snake_game_text = "Snake Game"
        draw_text(snake_game_text, snake_game_font, snake_game_color, screen, screen_width // 2, 80, center=True)

        made_by_font = pygame.font.Font(None, 70)  
        made_by_text = "Made by Vikas Sharma"
        draw_text(made_by_text, made_by_font, name_color, screen, screen_width // 2, 180, center=True)

        heading_text = "MAIN MENU"
        main_menu_y_position = screen_height // 4 + 100  
        draw_text(heading_text, heading_font, heading_color, screen, screen_width // 2, main_menu_y_position)
        heading_text_surface = heading_font.render(heading_text, True, heading_color)
        heading_rect = pygame.Rect(
            (screen_width // 2) - (heading_text_surface.get_width() // 2) - 20,
            main_menu_y_position - (heading_text_surface.get_height() // 2) - 20,  
            heading_text_surface.get_width() + 40,
            heading_text_surface.get_height() + 40,
        )
        pygame.draw.rect(screen, heading_color, heading_rect, border_radius=15, width=3)

        button_positions = [
            ((screen_width // 2) - (button_width // 2), (screen_height // 2) + 120 - 114),  
            ((screen_width // 2) - (button_width // 2), (screen_height // 2) + 200 - 114),  
        ]

        mouse_pos = pygame.mouse.get_pos()
        for i, (x, y) in enumerate(button_positions):
            hover = x <= mouse_pos[0] <= x + button_width and y <= mouse_pos[1] <= y + button_height
            draw_shadowed_button(
                x, y, button_width, button_height, buttons[i], hover, button_shadow_color, button_color, button_hover_color, button_font
            )

        instruction_rect = pygame.Rect(
            (screen_width // 2) - 200, screen_height - 160, 400, 120  
        )
        pygame.draw.rect(screen, text_color, instruction_rect, border_radius=10, width=2) 

        for i, line in enumerate(instructions):
            draw_text(line, instruction_font, text_color, screen, screen_width // 2, screen_height - 130 + (i * 30))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    if button_positions[0][0] <= mouse_pos[0] <= button_positions[0][0] + button_width and \
                            button_positions[0][1] <= mouse_pos[1] <= button_positions[0][1] + button_height:
                        # Launch Classic Game
                        import classic
                        classic.main()

                    if button_positions[1][0] <= mouse_pos[0] <= button_positions[1][0] + button_width and \
                            button_positions[1][1] <= mouse_pos[1] <= button_positions[1][1] + button_height:
                        # Launch Box Game
                        import level1
                        level1.main()  

        pygame.display.update()
        clock.tick(60)

main_menu()

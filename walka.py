import pygame

def draw_walka(screen, WIDTH, HEIGHT, font_path):
    font = pygame.font.Font(font_path, 28)
    text = font.render("Tu będzie walka", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

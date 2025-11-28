import pygame
import os

ZIELONY = (29, 162, 84)
ZIELONY2 = (39, 46, 42)
CZARNY = (0, 0, 0)

def draw_sklep(screen, WIDTH, HEIGHT, font_path, punkty_gracza):
    font = pygame.font.Font(font_path, 28)
    text = font.render("Sklep", True, (255, 255, 255))
    screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))

    #licznik punktow gracza
    punkty_font = pygame.font.Font(font_path, 22)
    punkty_text = punkty_font.render(f"Punkty: {punkty_gracza}", True, (255, 255, 255))
    padding = 8
    punkty_x = 375-(punkty_text.get_width() + padding*2)
    punkty_y = 66
    rect = pygame.Rect(
        punkty_x - padding,
        punkty_y - padding,
        punkty_text.get_width() + padding * 2,
        punkty_text.get_height() + padding * 2
    )
    pygame.draw.rect(screen, ZIELONY2, rect, border_radius=8)
    pygame.draw.rect(screen, ZIELONY, rect, width=3, border_radius=8)
    punkty_text = punkty_font.render(f"Punkty: {punkty_gracza}", True, (255, 255, 255))
    screen.blit(punkty_text, (punkty_x, punkty_y))

    #sklepikarz
    shop_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep.png")
    shop_img = pygame.image.load(shop_path).convert_alpha()
    screen.blit(shop_img, (0, 0))




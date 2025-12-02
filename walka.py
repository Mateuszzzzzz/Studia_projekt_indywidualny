import pygame
import os

#kolorki
ZIELONY = (29, 162, 84)
ZIELONY2 = (39, 46, 42)
BIALY = (255, 255, 255)
SZARY = (132, 126, 135)

#staty wrogow
enemy_stats = {
    1: {"DMG": 2, "HP": 30, "Nazwa": "Niebieski szlam"},
    2: {"DMG": 5, "HP": 50, "Nazwa": "Szkielet"},
    3: {"DMG": 15, "HP": 160, "Nazwa": "Wielki pająk"},
    4: {"DMG": 33, "HP": 400, "Nazwa": "Kamienny golem"},
    5: {"DMG": 65, "HP": 890, "Nazwa": "Żrąca Kostka"},
    6: {"DMG": 90, "HP": 1600, "Nazwa": "Głębinowy Koszmar"},
    7: {"DMG": 140, "HP": 4000, "Nazwa": "Szalony Arcymag"},
    8: {"DMG": 250, "HP": 9999, "Nazwa": "Pozaziemska Abominacja"},
    9: {"DMG": 630, "HP": 25000, "Nazwa": "Serce Świata"},
    10: {"DMG": 2150, "HP": 100000, "Nazwa": "Stworzyciel"},
    11: {"DMG": 6000, "HP": 500000, "Nazwa": "Źródło"},
}


def fit_text_to_width(text, font_path, max_width, max_size, min_size=10):
    size = max_size
    while size >= min_size:
        font = pygame.font.Font(font_path, size)
        if font.size(text)[0] <= max_width:
            return font.render(text, True, BIALY)
        size -= 1

    font = pygame.font.Font(font_path, min_size)
    return font.render(text, True, BIALY)


def split_enemy_name(name):
    words = name.split(" ")
    if len(words) == 1:
        return [name]
    elif len(words) == 2:
        return words
    else:
        mid = len(words) // 2
        return [" ".join(words[:mid]), " ".join(words[mid:])]


def draw_centered_text(screen, font, lines, color, box_x, box_y, box_w, padding):
    total_height = sum(font.size(line)[1] for line in lines) + (len(lines)-1)*4
    start_y = box_y + padding

    y = start_y
    for line in lines:
        rendered = font.render(line, True, color)
        x = box_x + (box_w - rendered.get_width()) // 2
        screen.blit(rendered, (x, y))
        y += rendered.get_height() + 4

    return total_height


def draw_walka(screen, WIDTH, HEIGHT, font_path, DMG_Gracza, HP_Gracza, Wrog_ID):
    #tło walki
    walka_bg_path = os.path.join(os.path.dirname(__file__), "Grafika", "Walka.png")
    walka_img = pygame.image.load(walka_bg_path).convert_alpha()
    screen.blit(walka_img, (0, 0))

    #przycisk wroga grafa
    klik_path = os.path.join(os.path.dirname(__file__), "Grafika", "Walcz.png")
    klik_img = pygame.image.load(klik_path).convert_alpha()

    #staty gracza
    punkt_font = pygame.font.Font(font_path, 40)
    padding = 8

    nazwa_text = punkt_font.render(" Gracz", True, BIALY)
    dmg_text = fit_text_to_width(f"DMG: {DMG_Gracza}", font_path, 220, 40)
    hp_text = fit_text_to_width(f"HP: {HP_Gracza}", font_path, 220, 40)

    box_w = max(nazwa_text.get_width(), dmg_text.get_width(), hp_text.get_width()) + padding * 2
    box_h = nazwa_text.get_height() + dmg_text.get_height() + hp_text.get_height() + padding * 4
    box_x = 20
    box_y = 488

    pygame.draw.rect(screen, ZIELONY2, (box_x, box_y, box_w, box_h), border_radius=10)
    pygame.draw.rect(screen, SZARY, (box_x, box_y, box_w, box_h), 3, border_radius=10)

    screen.blit(nazwa_text, (box_x + padding, box_y + padding))
    screen.blit(dmg_text, (box_x + padding, box_y + padding + nazwa_text.get_height() + 4))
    screen.blit(hp_text, (box_x + padding, box_y + padding + nazwa_text.get_height() +
                          dmg_text.get_height() + 8))

    #staty wroga
    nazwa_wroga = enemy_stats[Wrog_ID]["Nazwa"]
    DMG_wroga = enemy_stats[Wrog_ID]["DMG"]
    HP_wroga = enemy_stats[Wrog_ID]["HP"]

    wrog_box_w = box_w
    wrog_box_h = box_h
    wrog_box_x = WIDTH - wrog_box_w - 20
    wrog_box_y = 488

    pygame.draw.rect(screen, ZIELONY2, (wrog_box_x, wrog_box_y, wrog_box_w, wrog_box_h), border_radius=10)
    pygame.draw.rect(screen, SZARY, (wrog_box_x, wrog_box_y, wrog_box_w, wrog_box_h), 3, border_radius=10)

    wrog_font = pygame.font.Font(font_path, 26)
    lines = split_enemy_name(nazwa_wroga)
    draw_centered_text(screen, wrog_font, lines, BIALY, wrog_box_x, wrog_box_y, wrog_box_w, padding)

    wrog_dmg_text = fit_text_to_width(f"DMG: {DMG_wroga}", font_path, wrog_box_w - 20, 40)
    wrog_hp_text = fit_text_to_width(f"HP: {HP_wroga}", font_path, wrog_box_w - 20, 40)

    start_stats_y = wrog_box_y + padding + nazwa_text.get_height() + 4

    screen.blit(wrog_dmg_text, (wrog_box_x + padding, start_stats_y))
    screen.blit(wrog_hp_text, (wrog_box_x + padding, start_stats_y + wrog_dmg_text.get_height() + 4))

    #grafika wroga
    enemy_img_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Walka_wrog{Wrog_ID}.png")

    if os.path.isfile(enemy_img_path):
        enemy_img = pygame.image.load(enemy_img_path).convert_alpha()

        enemy_x = (WIDTH - enemy_img.get_width()) // 2
        enemy_y = 100

        screen.blit(enemy_img, (enemy_x, enemy_y))

    #przycisk od walki
    klik_x = (box_x + wrog_box_x - 25) // 2
    klik_y = box_y - klik_img.get_height() - 10
    screen.blit(klik_img, (klik_x, klik_y))

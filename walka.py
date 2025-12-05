import pygame
import os
import math
import sqlite3

#kolorki
ZIELONY = (29, 162, 84)
ZIELONY2 = (39, 46, 42)
BIALY = (255, 255, 255)
SZARY = (132, 126, 135)
CZERWONY = (255, 60, 60)

#stany dla walki
walka_stan = "idle"
walka_gracz_hp = None
walka_wrog_hp = None
walka_anim_timer = 0
hit_flash_alpha = 0
wrog_hit = False
gracz_hit = False
tura_delay = 0

#staty wrogow
enemy_stats = {
    1: {"DMG": 2, "HP": 30, "Nazwa": "Niebieski szlam"},
    2: {"DMG": 5, "HP": 50, "Nazwa": "Szkielet"},
    3: {"DMG": 15, "HP": 160, "Nazwa": "Wielki pająk"},
    4: {"DMG": 33, "HP": 400, "Nazwa": "Golem"},
    5: {"DMG": 65, "HP": 890, "Nazwa": "Żrąca Kostka"},
    6: {"DMG": 90, "HP": 1600, "Nazwa": "Głębinowy Koszmar"},
    7: {"DMG": 140, "HP": 4000, "Nazwa": "Szalony Arcymag"},
    8: {"DMG": 250, "HP": 9999, "Nazwa": "Pozaziemska Abominacja"},
    9: {"DMG": 630, "HP": 25000, "Nazwa": "Serce Świata"},
    10: {"DMG": 2150, "HP": 100000, "Nazwa": "Śniący"},
    11: {"DMG": 6000, "HP": 500000, "Nazwa": "Przebudzony"},
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
    y = box_y + padding

    for line in lines:
        rendered = font.render(line, True, color)
        x = box_x + (box_w - rendered.get_width()) // 2
        screen.blit(rendered, (x, y))
        y += rendered.get_height() + 4

    return total_height


#walka turowa
def walka_tick(DMG_Gracza, HP_Gracza, Wrog_ID):
    global walka_stan, walka_gracz_hp, walka_wrog_hp
    global wrog_hit, gracz_hit, hit_flash_alpha
    global tura_delay

    if tura_delay > 0:
        tura_delay -= 1
        return

    # Atak gracza
    if walka_stan == "gracz_atakuje":
        walka_wrog_hp -= DMG_Gracza
        wrog_hit = True
        hit_flash_alpha = 255
        tura_delay = 5

        if walka_wrog_hp <= 0:
            walka_stan = "koniec_wygrana"
        else:
            walka_stan = "wrog_atakuje"

    # Atak wroga
    elif walka_stan == "wrog_atakuje":
        DMG_wroga = enemy_stats[Wrog_ID]["DMG"]
        walka_gracz_hp -= DMG_wroga
        gracz_hit = True
        hit_flash_alpha = 255
        tura_delay = 5

        if walka_gracz_hp <= 0:
            walka_stan = "koniec_przegrana"
        else:
            walka_stan = "gracz_atakuje"


def get_current_enemy_id():
    db_path = os.path.join("baza_danych", "baza_danych.db")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT Obecny_Wróg FROM gracz WHERE ID_Gracza = 1")
    enemy_id = cur.fetchone()[0]
    conn.close()
    return enemy_id

def draw_walka(screen, WIDTH, HEIGHT, font_path, DMG_Gracza, HP_Gracza):
    global walka_stan, walka_gracz_hp, walka_wrog_hp
    global hit_flash_alpha, wrog_hit, gracz_hit
    Wrog_ID = get_current_enemy_id()

    if walka_gracz_hp is None:
        walka_gracz_hp = HP_Gracza
        walka_wrog_hp = enemy_stats[Wrog_ID]["HP"]

    #rysowanie tła
    walka_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Walka.png")).convert_alpha()
    screen.blit(walka_img, (0, 0))

    # przycisk walcz grafika
    klik_img = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Walcz.png")).convert_alpha()

    #pola statystyk gracza
    punkt_font = pygame.font.Font(font_path, 40)
    padding = 8

    nazwa_text = punkt_font.render(" Gracz", True, BIALY)
    dmg_text = fit_text_to_width(f"DMG: {DMG_Gracza}", font_path, 220, 40)
    hp_text = fit_text_to_width(f"HP: {walka_gracz_hp}", font_path, 220, 40)

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

    wrog_box_x = WIDTH - box_w - 20
    wrog_box_y = 488

    pygame.draw.rect(screen, ZIELONY2, (wrog_box_x, wrog_box_y, box_w, box_h), border_radius=10)
    pygame.draw.rect(screen, SZARY, (wrog_box_x, wrog_box_y, box_w, box_h), 3, border_radius=10)

    wrog_font = pygame.font.Font(font_path, 26)
    lines = split_enemy_name(nazwa_wroga)
    draw_centered_text(screen, wrog_font, lines, BIALY, wrog_box_x, wrog_box_y, box_w, padding)

    wrog_dmg_text = fit_text_to_width(f"DMG: {DMG_wroga}", font_path, box_w - 20, 40)
    wrog_hp_text = fit_text_to_width(f"HP: {walka_wrog_hp}", font_path, box_w - 20, 40)

    start_stats_y = wrog_box_y + padding + nazwa_text.get_height() + 4

    screen.blit(wrog_dmg_text, (wrog_box_x + padding, start_stats_y))
    screen.blit(wrog_hp_text, (wrog_box_x + padding, start_stats_y + wrog_dmg_text.get_height() + 4))

    #grafika wroga
    enemy_img_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Walka_wrog{Wrog_ID}.png")

    if os.path.isfile(enemy_img_path):
        enemy_img = pygame.image.load(enemy_img_path).convert_alpha()

        enemy_x = WIDTH // 2 - enemy_img.get_width() // 2
        enemy_y = 90 if Wrog_ID != 9 else 70

        #wrog dostal dmg efekt
        if wrog_hit:
            shake = int(5 * math.sin(pygame.time.get_ticks() * 0.2))
            enemy_x += shake
            enemy_y += shake

        screen.blit(enemy_img, (enemy_x, enemy_y))

        if wrog_hit:
            red_tint_strength = min(hit_flash_alpha, 90)
            tinted = enemy_img.copy()
            tinted.fill((red_tint_strength, 0, 0, 0), special_flags=pygame.BLEND_RGBA_ADD)
            screen.blit(tinted, (enemy_x, enemy_y))
            hit_flash_alpha -= 50
            if hit_flash_alpha <= 0:
                wrog_hit = False

    #przycisk walcz
    klik_x = (box_x + wrog_box_x - 35) // 2
    klik_y = box_y - klik_img.get_height() - 10
    screen.blit(klik_img, (klik_x, klik_y))

    mx, my = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()[0]

    if click and klik_img.get_rect(topleft=(klik_x, klik_y)).collidepoint(mx, my):
        if walka_stan == "idle":
            walka_stan = "gracz_atakuje"
        elif walka_stan in ["koniec_wygrana", "koniec_przegrana"]:
            walka_stan = "idle"
            walka_gracz_hp = None  # reset walki

    if walka_stan in ["gracz_atakuje", "wrog_atakuje"]:
        walka_tick(DMG_Gracza, HP_Gracza, Wrog_ID)

    if walka_stan == "koniec_wygrana":
        font = pygame.font.Font(font_path, 50)
        win_text = font.render("POKONANO WROGA!", True, ZIELONY)
        screen.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 50))
        # update DB:
        db_path = os.path.join("baza_danych", "baza_danych.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute("UPDATE gracz SET Obecny_Wróg = Obecny_Wróg + 1 WHERE ID_Gracza = 1")
        conn.commit()
        conn.close()
        walka_stan = "idle"
        walka_gracz_hp = None
        walka_wrog_hp = None

    if walka_stan == "koniec_przegrana":
        font = pygame.font.Font(font_path, 50)
        lose_text = font.render("PRZEGRAŁEŚ!", True, CZERWONY)
        screen.blit(lose_text, (WIDTH//2 - lose_text.get_width()//2, 50))

    return walka_gracz_hp, walka_wrog_hp, walka_stan

import pygame
import os
import random

ILE_ITEMOW = 101
ZIELONY = (29, 162, 84)
ZIELONY2 = (39, 46, 42)
CZARNY = (0, 0, 0)
SZARY = (150, 150, 150)
BIALY = (255, 255, 255)


#staty itemow
item_stats = {
    1: {"DMG": 2, "HP": 0, "Cena": 25, "Nazwa": "Miecz"},
    2: {"DMG": 0, "HP": 5, "Cena": 20, "Nazwa": "Tarcza"},
    3: {"DMG": 0, "HP": 23, "Cena": 80, "Nazwa": "Żelazna zbroja"},
    4: {"DMG": 0, "HP": 15, "Cena": 50, "Nazwa": "Żelazna hełm"},
    5: {"DMG": 0, "HP": 8, "Cena": 33, "Nazwa": "Żelazne buty"},
    6: {"DMG": 1, "HP": 0, "Cena": 15, "Nazwa": "Naszyjnik siły"},
    7: {"DMG": 0, "HP": 3, "Cena": 10, "Nazwa": "Naszyjnik wytrzymałości"},
    8: {"DMG": 0, "HP": 12, "Cena": 30, "Nazwa": "Naszyjnik zdrowia"},
    9: {"DMG": 1, "HP": 5, "Cena": 35, "Nazwa": "Czerwony kamień"},
    10: {"DMG": 4, "HP": 0, "Cena": 50, "Nazwa": "Rapier"},
    11: {"DMG": 2, "HP": 15, "Cena": 70, "Nazwa": "Nietoperz"},
    12: {"DMG": 6, "HP": 0, "Cena": 75, "Nazwa": "Księga wody"},
    13: {"DMG": 15, "HP": -20, "Cena": 125, "Nazwa": "Starożytana kamienna maska"},
    14: {"DMG": 1, "HP": 2, "Cena": 10, "Nazwa": "Trąbka"},
    15: {"DMG": 2, "HP": 0, "Cena": 25, "Nazwa": "Pierścień siły"},
    16: {"DMG": 0, "HP": 8, "Cena": 25, "Nazwa": "Pierścień zdrowia"},
    17: {"DMG": 0, "HP": 4, "Cena": 15, "Nazwa": "Pierścień wytrzymałości"},
    18: {"DMG": 0, "HP": 75, "Cena": 150, "Nazwa": "Kamienne serce"},
    19: {"DMG": 0, "HP": 0, "Cena": 1500, "Nazwa": "Magiczny grzyb"},
    20: {"DMG": 1, "HP": 8, "Cena": 30, "Nazwa": "Zielony grzyb"},
    21: {"DMG": 2, "HP": 40, "Cena": 90, "Nazwa": "Bong-Bing"},
    22: {"DMG": 0, "HP": 5, "Cena": 19, "Nazwa": "Cukierek"},
    23: {"DMG": 5, "HP": -10, "Cena": 60, "Nazwa": "Kaktus"},
    24: {"DMG": 100, "HP": 100, "Cena": 1, "Nazwa": "NIESAMOWITY Kaktus"},
    25: {"DMG": 0, "HP": 0, "Cena": 1500, "Nazwa": "Czapka bohatera"},
    26: {"DMG": 3, "HP": 0, "Cena": 35, "Nazwa": "Cegła"},
    27: {"DMG": 1, "HP": 15, "Cena": 35, "Nazwa": "Mała mucha"},
    28: {"DMG": 25, "HP": 0, "Cena": 250, "Nazwa": "Pogromca krakena"},
    29: {"DMG": 0, "HP": 0, "Cena": 1500, "Nazwa": "O.S.S.P."},
    30: {"DMG": 3, "HP": 0, "Cena": 35, "Nazwa": "Toporek"},
    31: {"DMG": 0, "HP": 15, "Cena": 25, "Nazwa": "Banan"},
    32: {"DMG": 10, "HP": 0, "Cena": 125, "Nazwa": "Miecz traw"},
    33: {"DMG": 8, "HP": 0, "Cena": 80, "Nazwa": "Niebieski orb"},
    34: {"DMG": 10, "HP": 15, "Cena": 140, "Nazwa": "Kiścień"},
    35: {"DMG": 18, "HP": 15, "Cena": 150, "Nazwa": "Wielki pierścień siły"},
    36: {"DMG": 0, "HP": 0, "Cena": 1500, "Nazwa": "Złota kula"},
    37: {"DMG": 0, "HP": 15, "Cena": 50, "Nazwa": "Miedziana zbroja"},
    38: {"DMG": 0, "HP": 140, "Cena": 250, "Nazwa": "Złota zbroja"},
    39: {"DMG": 2, "HP": 3, "Cena": 50, "Nazwa": "Łuk"},
    40: {"DMG": 0, "HP": 5, "Cena": 5, "Nazwa": "Skórzane buty"},
    41: {"DMG": 6, "HP": 0, "Cena": 55, "Nazwa": "Magiczna laska"},
    42: {"DMG": 2, "HP": 1, "Cena": 15, "Nazwa": "Maczuga"},
    43: {"DMG": 2, "HP": 30, "Cena": 115, "Nazwa": "Hełm rycerza"},
    44: {"DMG": 4, "HP": 10, "Cena": 65, "Nazwa": "Niebieski kapelusz"},
    45: {"DMG": 5, "HP": 0, "Cena": 65, "Nazwa": "Czerwony kapelusz"},
    46: {"DMG": 0, "HP": 21, "Cena": 55, "Nazwa": "Czerwona mikstura"},
    47: {"DMG": 0, "HP": 14, "Cena": 35, "Nazwa": "Niebieska mikstura"},
    48: {"DMG": 0, "HP": 120, "Cena": 235, "Nazwa": "Wielka mikstura"},
    49: {"DMG": 0, "HP": 95, "Cena": 190, "Nazwa": "Złote buty"},
    50: {"DMG": 0, "HP": 0, "Cena": 1500, "Nazwa": "Joker"},
    51: {"DMG": 10, "HP": 0, "Cena": 95, "Nazwa": "Blaster"},
    52: {"DMG": 10, "HP": 95, "Cena": 300, "Nazwa": "Złoty naszyjnik"},
    53: {"DMG": 10, "HP": -5, "Cena": 80, "Nazwa": "Niedźwiedzie sidła"},
    54: {"DMG": 12, "HP": 0, "Cena": 140, "Nazwa": "Ogień"},
    55: {"DMG": 0, "HP": 240, "Cena": 350, "Nazwa": "Chitynowa zbroja"},
    56: {"DMG": 0, "HP": 190, "Cena": 300, "Nazwa": "Chitynowy hełm"},
    57: {"DMG": 30, "HP": 0, "Cena": 350, "Nazwa": "Niesamowicie wielki miecz"},
    58: {"DMG": 33, "HP": 3, "Cena": 380, "Nazwa": "Horyzont zdarzeń"},
    59: {"DMG": 1, "HP": 0, "Cena": 10, "Nazwa": "Kamień"},
    60: {"DMG": 8, "HP": 20, "Cena": 140, "Nazwa": "Płaszcz maga"},
    61: {"DMG": -2, "HP": 35, "Cena": 20, "Nazwa": "Kostur zdrowia"},
    62: {"DMG": 0, "HP": 60, "Cena": 60, "Nazwa": "Chrupiący posiłek"},
    63: {"DMG": 6, "HP": 0, "Cena": 60, "Nazwa": "Związek X"},
    64: {"DMG": 3, "HP": 15, "Cena": 50, "Nazwa": "Czapka pirata"},
    65: {"DMG": 0, "HP": 35, "Cena": 40, "Nazwa": "Brokuł"},
    66: {"DMG": 0, "HP": 0, "Cena": 0, "Nazwa": "Pudełko niespodzianka"},
    67: {"DMG": 0, "HP": 20, "Cena": 20, "Nazwa": "Jabłko"},
    68: {"DMG": 0, "HP": 18, "Cena": 60, "Nazwa": "Żelazna tarcza"},
    69: {"DMG": 5, "HP": 5, "Cena": 75, "Nazwa": "Różdzka lodu"},
    70: {"DMG": 8, "HP": 0, "Cena": 75, "Nazwa": "Topór"},
    71: {"DMG": 31, "HP": 0, "Cena": 360, "Nazwa": "Armata"},
    72: {"DMG": 1, "HP": 10, "Cena": 20, "Nazwa": "Marchewka"},
    73: {"DMG": 3, "HP": 7, "Cena": 35, "Nazwa": "Kawał mięsa"},
    74: {"DMG": 20, "HP": 0, "Cena": 240, "Nazwa": "Księga ognia"},
    75: {"DMG": 0, "HP": 30, "Cena": 30, "Nazwa": "Pomarańcza"},
    76: {"DMG": 0, "HP": 170, "Cena": 270, "Nazwa": "Chitynowe buty"},
    77: {"DMG": 8, "HP": 0, "Cena": 70, "Nazwa": "Kordelas"},
    78: {"DMG": 14, "HP": 0, "Cena": 140, "Nazwa": "Długi miecz"},
    79: {"DMG": 13, "HP": 0, "Cena": 135, "Nazwa": "Zdobiony łuk"},
    80: {"DMG": 4, "HP": 0, "Cena": 45, "Nazwa": "Włócznia"},
    81: {"DMG": 0, "HP": 333, "Cena": 460, "Nazwa": "Owoc życia"},
    82: {"DMG": 0, "HP": 240, "Cena": 370, "Nazwa": "Chitynowe tarcza"},
    83: {"DMG": 7, "HP": 40, "Cena": 170, "Nazwa": "Dziwny klejnot"},
    84: {"DMG": 6, "HP": 0, "Cena": 70, "Nazwa": "Buława"},
    85: {"DMG": 30, "HP": 0, "Cena": 370, "Nazwa": "Różdżka nekromanty"},
    86: {"DMG": 0, "HP": 150, "Cena": 250, "Nazwa": "Magiczna tarcza"},
    87: {"DMG": 3, "HP": 0, "Cena": 25, "Nazwa": "Czerwona chusta"},
    88: {"DMG": 0, "HP": 15, "Cena": 25, "Nazwa": "Zielona chusta"},
    89: {"DMG": 2, "HP": 12, "Cena": 45, "Nazwa": "Sierp"},
    90: {"DMG": 20, "HP": 150, "Cena": 435, "Nazwa": "Czerwony miecz"},
    91: {"DMG": 30, "HP": 20, "Cena": 400, "Nazwa": "Kostur piorunów"},
    92: {"DMG": 10, "HP": 50, "Cena": 200, "Nazwa": "Kwiecista korona"},
    93: {"DMG": 35, "HP": 100, "Cena": 500, "Nazwa": "Spadajaca gwiazda"},
    94: {"DMG": 45, "HP": 250, "Cena": 650, "Nazwa": "Kolor nie z tego świata"},
    95: {"DMG": 0, "HP": 131, "Cena": 220, "Nazwa": "Obronny medialion"},
    96: {"DMG": 65, "HP": 0, "Cena": 630, "Nazwa": "Największy miecz"},
    97: {"DMG": 75, "HP": 50, "Cena": 750, "Nazwa": "Wszystko widzące oko"},
    98: {"DMG": 8, "HP": 15, "Cena": 85, "Nazwa": "Róża"},
    99: {"DMG": 45, "HP": 315, "Cena": 700, "Nazwa": "Berło gwiazd"},
    100: {"DMG": 3, "HP": 45, "Cena": 80, "Nazwa": "Kaptur maga"},
    101: {"DMG": 9, "HP": 5, "Cena": 100, "Nazwa": "Fajerwerek"},
}

selected_item = None
selected_slot = None
show_window = False

if not hasattr(__import__("builtins"), "draw_sklep_prev_mouse"):
    __import__("builtins").draw_sklep_prev_mouse = False

def draw_item_window(screen, font_path, item_id, WIDTH, HEIGHT):
    font = pygame.font.Font(font_path, 26)
    w, h = 300, 380
    x, y = WIDTH - w - 20, 120
    pygame.draw.rect(screen, BIALY, (x, y, w, h), border_radius=12)
    pygame.draw.rect(screen, ZIELONY2, (x, y, w, h), 3, border_radius=12)

    stats = item_stats[item_id]
    img_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{item_id:03d}.png")
    try:
        img = pygame.image.load(img_path).convert_alpha()
    except Exception:
        img = pygame.Surface((80, 80), pygame.SRCALPHA)
        pygame.draw.rect(img, (200,200,200), img.get_rect())
    screen.blit(img, (x + (w - img.get_width())//2, y + 10))

    #staty itemow
    screen.blit(font.render(stats["Nazwa"], True, CZARNY), (x + 20, y + 120))
    screen.blit(font.render(f"Cena: {stats['Cena']}", True, CZARNY), (x + 20, y + 160))
    screen.blit(font.render(f"DMG: {stats['DMG']}", True, CZARNY), (x + 20, y + 200))
    screen.blit(font.render(f"HP: {stats['HP']}", True, CZARNY), (x + 20, y + 240))

    kup_rect = pygame.Rect(x + 20, y + 290, 120, 40)
    anuluj_rect = pygame.Rect(x + 160, y + 290, 120, 40)

    pygame.draw.rect(screen, (0, 120, 0), kup_rect, border_radius=10)
    pygame.draw.rect(screen, (120, 0, 0), anuluj_rect, border_radius=10)

    mx, my = pygame.mouse.get_pos()

    #kup
    if kup_rect.collidepoint(mx, my):
        kup_color = (ZIELONY)
        kup_text_color = (CZARNY)
    else:
        kup_color = (SZARY)
        kup_text_color = (BIALY)

    pygame.draw.rect(screen, kup_color, kup_rect, border_radius=10)

    kup_text = font.render("Kup", True, kup_text_color)
    kup_text_x = kup_rect.centerx - kup_text.get_width() // 2
    kup_text_y = kup_rect.centery - kup_text.get_height() // 2
    screen.blit(kup_text, (kup_text_x, kup_text_y))

    #anuluj
    if anuluj_rect.collidepoint(mx, my):
        anuluj_color = (ZIELONY)
        anuluj_text_color = (CZARNY)
    else:
        anuluj_color = (SZARY)
        anuluj_text_color = (BIALY)

    pygame.draw.rect(screen, anuluj_color, anuluj_rect, border_radius=10)

    anuluj_text = font.render("Anuluj", True, anuluj_text_color)
    anuluj_text_x = anuluj_rect.centerx - anuluj_text.get_width() // 2
    anuluj_text_y = anuluj_rect.centery - anuluj_text.get_height() // 2
    screen.blit(anuluj_text, (anuluj_text_x, anuluj_text_y))

    return kup_rect, anuluj_rect

def draw_sklep(screen, WIDTH, HEIGHT, font_path, punkty_gracza, ukonczone_zadania, DMG_Gracza, HP_Gracza):
    global selected_item, show_window, selected_slot, window_block_click
    prev_mouse = __import__("builtins").draw_sklep_prev_mouse

    #specjalne itemy!!
        #grzyb
    if 19 in item_stats:
        item_stats[19]["DMG"] = DMG_Gracza + round(DMG_Gracza/2)
        item_stats[19]["HP"] = round(HP_Gracza/3)
    if 25 in item_stats:
        item_stats[25]["DMG"] = DMG_Gracza*3
    if 29 in item_stats:
        item_stats[29]["HP"] = HP_Gracza*5
    if 36 in item_stats:
        item_stats[36]["DMG"] = round(HP_Gracza/2)
        item_stats[36]["HP"] = round(DMG_Gracza/2)
    if 50 in item_stats:
        item_stats[50]["DMG"] = round(DMG_Gracza*random.randint(1,6)/random.randint(1,3))
        item_stats[50]["HP"] = round(HP_Gracza*random.randint(1,6)/random.randint(1,3))
    if 66 in item_stats:
        item_stats[66]["DMG"] = round(random.randint(1,6)*random.randint(1,6))
        item_stats[66]["HP"] = round(random.randint(1,6)*random.randint(1,6))
        item_stats[66]["Cena"] = round(random.randint(1,6)*random.randint(1,6)*random.randint(1,6))

    shop_bg_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep.png")
    shop_img = pygame.image.load(shop_bg_path).convert_alpha()
    screen.blit(shop_img, (0, 0))

    #staty gracza
    punkt_font = pygame.font.Font(font_path, 18)
    padding = 8
    punkty_text = punkt_font.render(f"Punkty: {punkty_gracza}", True, (255,255,255))
    dmg_text = punkt_font.render(f"DMG: {DMG_Gracza}", True, (255,255,255))
    hp_text = punkt_font.render(f"HP: {HP_Gracza}", True, (255,255,255))

    box_w = max(punkty_text.get_width(), dmg_text.get_width(), hp_text.get_width()) + padding*2
    box_h = punkty_text.get_height() + dmg_text.get_height() + hp_text.get_height() + padding*4
    box_x = WIDTH - box_w - 20
    box_y = 78

    pygame.draw.rect(screen, ZIELONY2, (box_x, box_y, box_w, box_h), border_radius=10)
    pygame.draw.rect(screen, ZIELONY, (box_x, box_y, box_w, box_h), 3, border_radius=10)

    screen.blit(punkty_text, (box_x + padding, box_y + padding))
    screen.blit(dmg_text, (box_x + padding, box_y + padding + punkty_text.get_height() + 4))
    screen.blit(hp_text, (box_x + padding, box_y + padding + punkty_text.get_height() + dmg_text.get_height() + 8))

    item_rects = []
    pozycje_x = [10, 84, 158, 232, 306]
    rzad_y = [310, 384, 458, 532, 606]

    #blokady
    blokada_img1 = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada1.png")).convert_alpha()
    blokada_img2 = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada2.png")).convert_alpha()
    blokada_img3 = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada3.png")).convert_alpha()
    blokada_img4 = pygame.image.load(os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada4.png")).convert_alpha()

    for n in range(1, 26):
        attr = f"item{n}ran"
        if not hasattr(draw_sklep, attr):
            setattr(draw_sklep, attr, random.randint(1, ILE_ITEMOW))

    for row in range(5):
        locked = False
        if row == 1 and ukonczone_zadania < 10:
            locked = True
            blok_img = blokada_img1
        elif row == 2 and ukonczone_zadania < 20:
            locked = True
            blok_img = blokada_img2
        elif row == 3 and ukonczone_zadania < 50:
            locked = True
            blok_img = blokada_img3
        elif row == 4 and ukonczone_zadania < 99:
            locked = True
            blok_img = blokada_img4
        else:
            blok_img = None

        if locked and blok_img:
            target_w = pozycje_x[-1] + 125 - pozycje_x[0]
            target_w = WIDTH+7
            target_h = blok_img.get_height()
            scaled = pygame.transform.smoothscale(blok_img, (target_w, target_h))
            screen.blit(scaled, (10, rzad_y[row]))
            continue

        for col in range(5):
            n = row*5 + col + 1
            item_id = getattr(draw_sklep, f"item{n}ran")
            if item_id is None:
                continue

            pos = (pozycje_x[col], rzad_y[row])
            img_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{item_id:03d}.png")
            img = pygame.image.load(img_path).convert_alpha()
            screen.blit(img, pos)

            rect = pygame.Rect(pos[0], pos[1], img.get_width(), img.get_height())
            item_rects.append((rect, item_id, n))

    mx, my = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()[0]
    clicked_now = mouse_pressed and (not prev_mouse)
    __import__("builtins").draw_sklep_prev_mouse = mouse_pressed

    if clicked_now and not show_window:
        for rect, item_id, slot_n in item_rects:
            if rect.collidepoint(mx, my):
                selected_item = item_id
                selected_slot = slot_n
                show_window = True
                window_block_click = True
                break

    #okno zakupu
    if show_window and selected_item is not None:
        kup_rect, anuluj_rect = draw_item_window(screen, font_path, selected_item, WIDTH, HEIGHT)

        if window_block_click:
            if not mouse_pressed:
                window_block_click = False
            return punkty_gracza, DMG_Gracza, HP_Gracza

        if clicked_now:
            if kup_rect.collidepoint(mx, my):
                cena = item_stats[selected_item]["Cena"]
                if punkty_gracza >= cena:
                    punkty_gracza -= cena
                    DMG_Gracza += item_stats[selected_item]["DMG"]
                    HP_Gracza += item_stats[selected_item]["HP"]
                    import sqlite3
                    db_path = os.path.join("baza_danych", "baza_danych.db")
                    conn = sqlite3.connect(db_path)
                    cursor = conn.cursor()

                    cursor.execute("""
                        UPDATE gracz
                        SET Doświadczenie_Gracza = Doświadczenie_Gracza - ?,
                            DMG_Gracza = DMG_Gracza + ?,
                            HP_Gracza = HP_Gracza + ?
                        WHERE ID_Gracza = ?
                    """, (cena, item_stats[selected_item]["DMG"], item_stats[selected_item]["HP"], 1))

                    conn.commit()
                    conn.close()

                    if selected_slot is not None and hasattr(draw_sklep, f"item{selected_slot}ran"):
                        setattr(draw_sklep, f"item{selected_slot}ran", None)

                    show_window = False
                    selected_item = None
                    selected_slot = None
                    window_block_click = False
                else:
                    show_window = False
                    selected_item = None
                    selected_slot = None
            elif anuluj_rect.collidepoint(mx, my):
                show_window = False
                selected_item = None
                selected_slot = None
                window_block_click = False
    return punkty_gracza, DMG_Gracza, HP_Gracza

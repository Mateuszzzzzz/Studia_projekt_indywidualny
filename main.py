import pygame
import sqlite3
import os
from datetime import datetime
from sklep import draw_sklep
from walka import draw_walka

pygame.init()

#Rozdzialka jak dla telefonu okna aplikacji zeby potem sie nie bawic w zmienianie tego przy portowaniu
WIDTH, HEIGHT = 375, 667
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lista zadań")

#Kolory uzywane w apce
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
FIOLET = (39, 46, 42)
FIOLET2 = (42, 73, 61)
ZIELONY = (29, 162, 84)
ZIELONY2 = (20, 114, 60)
SZARY = (150, 150, 150)
PRZYCIEMNIENIE = (0, 0, 0, 150)
PRZYCISK_BG = (160, 160, 160)
PRZYCISK_HOVER = (29, 162, 84)
AKTYWNE_POLE = (0, 255, 0)
JASNY_SZARY = (160, 160, 160)
BRAK_TYTULU_COLOR = (255, 0, 0)
BRAZ = (102, 57, 49)

#Ustawienia dla czcionki (moze potem zmienic te vt323 na jakas autorska jak starczy czasu?)
MAX_FONT_SIZE = 23
MIN_FONT_SIZE = 12
font_path = os.path.join(os.path.dirname(__file__), "Czcionka", "VT323-Regular.ttf")

#Baza danych apki
db_path = os.path.join("baza_danych", "baza_danych.db")
os.makedirs("baza_danych", exist_ok=True)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
#zadanka w bazie
cur.execute('''CREATE TABLE IF NOT EXISTS zadania (
    ID_Zadania INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa_zadania TEXT,
    Opis_zadania TEXT,
    Nagroda INTEGER DEFAULT 0,
    Data_dodania TEXT,
    Czy_zaliczone INTEGER DEFAULT 0,
    Data_do_końca TEXT
)''')
#staty gracza w bazie
cur.execute('''CREATE TABLE IF NOT EXISTS gracz (
    ID_Gracza INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa_Gracza TEXT,
    Poziom_Gracza INTEGER DEFAULT 1,
    Doświadczenie_Gracza INTEGER DEFAULT 0,
    HP_Gracza INTEGER DEFAULT 25,
    DMG_Gracza INTEGER DEFAULT 3
)''')
#stworzenie bazowego profilu gracza w bazie
cur.execute("SELECT COUNT(*) FROM gracz")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO gracz (Nazwa_Gracza) VALUES ('Gracz_tymczasowy_wersji_alpha')")
    conn.commit()

#ustawienie wartosci punkty gracza na wartosc z bazy
cur.execute("SELECT Doświadczenie_Gracza FROM gracz LIMIT 1")
row = cur.fetchone()
punkty_gracza = row[0] if row else 0

input_width = int(WIDTH * 0.85)
title_height, desc_height, reward_height = 50, 80, 40
MAX_TITLE_CHARS, MAX_DESC_CHARS, MAX_REWARD = 30, 60, 9999

active_field = None
show_input = False

#Grafika i pozycja dla przycisku dodawania nowych zadan
button_path = os.path.join(os.path.dirname(__file__), "Grafika", "Button.png")
button_hover_path = os.path.join(os.path.dirname(__file__), "Grafika", "Button_hover.png")
if os.path.exists(button_path):
    button_image = pygame.image.load(button_path).convert_alpha()
else:
    button_image = pygame.Surface((48, 48), pygame.SRCALPHA)
    pygame.draw.circle(button_image, BIALY, (24,24), 22)
if os.path.exists(button_hover_path):
    button_hover_image = pygame.image.load(button_hover_path).convert_alpha()
else:
    button_hover_image = button_image.copy()
button_rect = button_image.get_rect(topright=(WIDTH - 14, HEIGHT - 78))

#Zakladki u gory ekranu w apce
tabs = ["Zadania", "Sklep", "Walka"]
active_tab = "Zadania"
tab_height = 50
tab_width = WIDTH // len(tabs)
tab_font = pygame.font.Font(font_path, 24)

#Scroll listy zadan
scroll_y = 0
SCROLL_STEP = 35

#Funkcje pomocnicze
def get_fitting_font(text, max_width, max_font=MAX_FONT_SIZE, min_font=MIN_FONT_SIZE):
    font_size = max_font
    while font_size >= min_font:
        font = pygame.font.Font(font_path, font_size)
        if font.size(text)[0] <= max_width - 20:
            return font
        font_size -= 1
    return pygame.font.Font(font_path, min_font)

def wrap_text(text, font, max_width):
    words = text.split(' ')
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] <= max_width:
            current_line = test_line
        else:
            lines.append(current_line.strip())
            current_line = word + " "
    lines.append(current_line.strip())
    return lines

def load_tasks():
    cur.execute("SELECT * FROM zadania ORDER BY ID_Zadania DESC")
    rows = cur.fetchall()
    tasks_prepared = []
    for task in rows:
        font = get_fitting_font(task[1], WIDTH - 40)
        tasks_prepared.append({
            "id": task[0],
            "text": task[1],
            "completed": task[5],
            "font": font,
            "nagroda": task[3],
            "opis": task[2],
            "data": task[4]
        })
    return tasks_prepared

def add_task_to_db(title, desc, reward):
    if not title.strip() or title == "Tytuł...":
        return
    cur.execute("INSERT INTO zadania (Nazwa_zadania, Opis_zadania, Nagroda, Data_dodania) VALUES (?, ?, ?, ?)",
                (title, desc, reward, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def complete_task(task_id, reward):
    cur.execute("UPDATE zadania SET Czy_zaliczone = 1 WHERE ID_Zadania = ?", (task_id,))
    cur.execute("UPDATE gracz SET Doświadczenie_Gracza = Doświadczenie_Gracza + ?", (reward,))
    conn.commit()

tasks = load_tasks()
selected_task = None
show_details = False

running = True
clock = pygame.time.Clock()
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


        elif event.type == pygame.MOUSEBUTTONDOWN and event.button in (4, 5):
            if active_tab == "Zadania" and not show_input and not show_details:
                item_h = 35
                gap = 10
                aktywne = [t for t in tasks if t["completed"] == 0]
                wykonane = [t for t in tasks if t["completed"] == 1]
                content_height = (
                        10 +
                        30 + 15 +
                        len(aktywne) * (item_h + gap) +
                        20 +
                        30 + 15 +
                        len(wykonane) * (item_h + gap) +
                        40
                )
                visible_height = HEIGHT - (tab_height + 10)
                max_scroll = max(0, content_height - visible_height)
                if event.button == 4:
                    scroll_y = max(0, scroll_y - SCROLL_STEP)
                elif event.button == 5:
                    scroll_y = min(max_scroll, scroll_y + SCROLL_STEP)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, tab in enumerate(tabs):
                tab_rect = pygame.Rect(i * tab_width, 0, tab_width, tab_height)
                if tab_rect.collidepoint(event.pos):
                    active_tab = tab
                    show_input = False
                    active_field = None
                    scroll_y = 0
                    break

            if active_tab == "Zadania":
                if show_input:
                    form_width = 300
                    form_height = 290
                    form_rect = pygame.Rect(
                        (WIDTH - form_width) // 2,
                        (HEIGHT - form_height) // 2,
                        form_width,
                        form_height
                    )
                    inner_x = form_rect.x + 20
                    y_offset = form_rect.y + 20

                    title_rect_input = pygame.Rect(inner_x, y_offset, form_rect.width - 40, 45)
                    y_offset = title_rect_input.bottom + 12

                    desc_rect_input = pygame.Rect(inner_x, y_offset, form_rect.width - 40, 80)
                    y_offset = desc_rect_input.bottom + 10

                    reward_rect_input = pygame.Rect(inner_x, y_offset, (form_rect.width - 40)//2, 38)
                    y_offset = reward_rect_input.bottom + 10

                    add_rect_input = pygame.Rect(inner_x, y_offset, (form_rect.width - 50)//2, 36)
                    cancel_rect_input = pygame.Rect(add_rect_input.right + 20, y_offset, (form_rect.width - 50)//2, 36)

                    if title_rect_input.collidepoint(event.pos):
                        active_field = "title"
                        if input_title == "Tytuł...":
                            input_title = ""
                    elif desc_rect_input.collidepoint(event.pos):
                        active_field = "desc"
                        if input_desc == "Opis...":
                            input_desc = ""
                    elif reward_rect_input.collidepoint(event.pos):
                        active_field = "reward"
                        if input_reward == "0":
                            input_reward = ""
                    elif add_rect_input.collidepoint(event.pos) and input_title.strip() != "" and input_title != "Tytuł...":
                        reward_val = int(input_reward) if input_reward.isdigit() else 0
                        add_task_to_db(input_title, input_desc, reward_val)
                        tasks = load_tasks()
                        input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
                        show_input = False
                        active_field = None
                    elif cancel_rect_input.collidepoint(event.pos):
                        input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
                        show_input = False
                        active_field = None
                    else:
                        if not (title_rect_input.collidepoint(event.pos) or desc_rect_input.collidepoint(event.pos) or reward_rect_input.collidepoint(event.pos)):
                            active_field = None

                elif show_details and selected_task:
                    details_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 120, 300, 240)
                    if selected_task[5] == 0:
                        button_width = 100
                        button_height = 30
                        spacing = 30
                        total_width = button_width * 2 + spacing
                        start_x = details_rect.centerx - total_width // 2
                        done_rect = pygame.Rect(start_x, details_rect.bottom - 40, button_width, button_height)
                        close_rect = pygame.Rect(start_x + button_width + spacing, details_rect.bottom - 40, button_width, button_height)
                        if done_rect.collidepoint(event.pos):
                            complete_task(selected_task[0], selected_task[3])
                            tasks = load_tasks()
                            try:
                                punkty_gracza += int(selected_task[3])
                            except Exception:
                                pass
                            cur.execute("SELECT * FROM zadania WHERE ID_Zadania = ?", (selected_task[0],))
                            selected_task = cur.fetchone()
                        elif close_rect.collidepoint(event.pos):
                            show_details = False
                            selected_task = None
                    else:
                        close_rect = pygame.Rect(details_rect.centerx - 50, details_rect.bottom - 40, 100, 30)
                        if close_rect.collidepoint(event.pos):
                            show_details = False
                            selected_task = None

                else:
                    if not show_input and button_rect.collidepoint(event.pos) and not show_details:
                        show_input = True
                        input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
                    else:
                        for rect, task_id in task_positions:
                            if rect.collidepoint(event.pos):
                                cur.execute("SELECT * FROM zadania WHERE ID_Zadania = ?", (task_id,))
                                selected_task = cur.fetchone()
                                show_details = True
                                break

        elif event.type == pygame.KEYDOWN and show_input and active_field:
            char = event.unicode
            if active_field == "title":
                if event.key == pygame.K_BACKSPACE:
                    input_title = input_title[:-1]
                elif len(input_title) < MAX_TITLE_CHARS:
                    input_title += char
            elif active_field == "desc":
                if event.key == pygame.K_BACKSPACE:
                    input_desc = input_desc[:-1]
                elif len(input_desc) < MAX_DESC_CHARS:
                    input_desc += char
            elif active_field == "reward":
                if event.key == pygame.K_BACKSPACE:
                    input_reward = input_reward[:-1]
                elif char.isdigit() and (input_reward == "" or int(input_reward + char) <= MAX_REWARD):
                    input_reward += char


    task_area = pygame.Rect(0, tab_height, WIDTH, HEIGHT - tab_height)
    if active_tab == "Zadania":
        screen.fill(FIOLET)
    elif active_tab == "Sklep":
        screen.fill(BRAZ)
    elif active_tab == "Walka":
        screen.fill(JASNY_SZARY)
    task_positions = []

    if active_tab == "Zadania":
        y = tab_height + 10 - scroll_y
        item_h = 35
        gap = 10
        naglowek_font = pygame.font.Font(font_path, 22)

        aktywne = [t for t in tasks if t["completed"] == 0]
        wykonane = [t for t in tasks if t["completed"] == 1]

        task_positions = []

        start_y_aktywne = y+5

        text = naglowek_font.render("ZADANIA AKTYWNE", True, BIALY)
        screen.blit(text, (30, y))
        y += text.get_height() + 8

        start_y_aktywne = y + 5
        item_h = 35
        gap = 10
        outer_height = len(aktywne) * (item_h + gap) - gap + 20
        outer_rect_aktywne = pygame.Rect(20, start_y_aktywne - 10, WIDTH - 40, outer_height)

        pygame.draw.rect(screen, ZIELONY2, outer_rect_aktywne, border_radius=12)
        pygame.draw.rect(screen, BIALY, outer_rect_aktywne, 2, border_radius=12)

        y = start_y_aktywne
        for task in aktywne:
            text_surface = task["font"].render(task["text"], True, CZARNY)
            border_rect = pygame.Rect(30, y, WIDTH - 60, item_h)
            pygame.draw.rect(screen, BIALY, border_rect, border_radius=8)
            pygame.draw.rect(screen, FIOLET, border_rect, 2, border_radius=8)
            screen.blit(text_surface, (border_rect.x + 10, border_rect.y + 5))
            task_positions.append((border_rect, task["id"]))
            y += item_h + gap

        y += 20
        start_y_wykonane = y

        text = naglowek_font.render("ZADANIA WYKONANE", True, BIALY)
        screen.blit(text, (30, y))
        y += text.get_height() + 15

        item_h = 35
        gap = 10
        outer_height = len(wykonane) * (item_h + gap) - gap + 20
        outer_rect_wykonane = pygame.Rect(20, y - 10, WIDTH - 40, outer_height)
        pygame.draw.rect(screen, ZIELONY2, outer_rect_wykonane, border_radius=12)
        pygame.draw.rect(screen, BIALY, outer_rect_wykonane, 2, border_radius=12)

        for task in wykonane:
            text_surface = task["font"].render(task["text"], True, CZARNY)
            border_rect = pygame.Rect(30, y, WIDTH - 60, item_h)
            pygame.draw.rect(screen, ZIELONY, border_rect, border_radius=8)
            pygame.draw.rect(screen, BIALY, border_rect, 2, border_radius=8)
            screen.blit(text_surface, (border_rect.x + 10, border_rect.y + 5))
            task_positions.append((border_rect, task["id"]))
            y += item_h + gap

    screen.set_clip(None)

    for i, tab in enumerate(tabs):
        tab_rect = pygame.Rect(i * tab_width, 0, tab_width, tab_height)
        if tab == active_tab:
            pygame.draw.rect(screen, ZIELONY, tab_rect)
        elif tab_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, PRZYCISK_HOVER, tab_rect)
        else:
            pygame.draw.rect(screen, PRZYCISK_BG, tab_rect)
        pygame.draw.rect(screen, CZARNY, tab_rect, 2)
        text_surface = tab_font.render(tab, True, CZARNY)
        screen.blit(text_surface, (tab_rect.centerx - text_surface.get_width() // 2,

                                   tab_rect.centery - text_surface.get_height() // 2))
    if active_tab == "Zadania":
        current_button_img = button_hover_image if button_rect.collidepoint(mouse_pos) and not show_details else button_image
        if show_input:
            button_dim = current_button_img.copy()
            button_dim.fill((255, 255, 255, 100), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(button_dim, button_rect)
        else:
            screen.blit(current_button_img, button_rect)

        if show_input:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill(PRZYCIEMNIENIE)
            screen.blit(s, (0, 0))
            counter_font = pygame.font.Font(font_path, 14)

            form_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 160, 300, 290)
            pygame.draw.rect(screen, BIALY, form_rect, border_radius=12)
            pygame.draw.rect(screen, FIOLET2, form_rect, 2, border_radius=12)

            inner_x = form_rect.x + 20
            y_offset = form_rect.y + 20

            if active_field != "title" and (input_title.strip() == ""):
                title_border_color = BRAK_TYTULU_COLOR
            elif active_field == "title":
                title_border_color = AKTYWNE_POLE
            else:
                title_border_color = FIOLET2

            title_rect = pygame.Rect(inner_x, y_offset, form_rect.width - 40, 45)
            pygame.draw.rect(screen, (245, 245, 245), title_rect, border_radius=8)
            pygame.draw.rect(screen, title_border_color, title_rect, 2, border_radius=8)
            font_title = get_fitting_font(input_title, title_rect.width)
            color_title = CZARNY if input_title != "Tytuł..." else JASNY_SZARY
            screen.blit(font_title.render(input_title, True, color_title),
                        (title_rect.x + 10, title_rect.y + (title_rect.height - font_title.size(input_title)[1]) // 2))
            counter_surface = counter_font.render(f"{len(input_title)}/{MAX_TITLE_CHARS}", True, SZARY)
            screen.blit(counter_surface, (title_rect.right - counter_surface.get_width() - 5,
                                          title_rect.bottom - counter_surface.get_height() - 5))
            y_offset = title_rect.bottom + 12

            desc_border_color = AKTYWNE_POLE if active_field == "desc" else FIOLET2
            desc_rect = pygame.Rect(inner_x, y_offset, form_rect.width - 40, 80)
            pygame.draw.rect(screen, (245, 245, 245), desc_rect, border_radius=8)
            pygame.draw.rect(screen, desc_border_color, desc_rect, 2, border_radius=8)
            font_desc = get_fitting_font(input_desc, desc_rect.width, max_font=20)
            color_desc = CZARNY if input_desc != "Opis..." or active_field == "desc" else JASNY_SZARY

            desc_lines = wrap_text(input_desc, font_desc, desc_rect.width - 15)
            y_text = desc_rect.y + 6
            for line in desc_lines:
                screen.blit(font_desc.render(line, True, color_desc), (desc_rect.x + 8, y_text))
                y_text += font_desc.size(line)[1] + 2

            counter_surface = counter_font.render(f"{len(input_desc)}/{MAX_DESC_CHARS}", True, SZARY)
            screen.blit(counter_surface, (desc_rect.right - counter_surface.get_width() - 5,
                                          desc_rect.bottom - counter_surface.get_height() - 5))
            y_offset = desc_rect.bottom + 10

            reward_border_color = AKTYWNE_POLE if active_field == "reward" else FIOLET2
            reward_rect = pygame.Rect(inner_x, y_offset, (form_rect.width - 40)//2, 38)
            pygame.draw.rect(screen, (245, 245, 245), reward_rect, border_radius=8)
            pygame.draw.rect(screen, reward_border_color, reward_rect, 2, border_radius=8)
            font_reward = get_fitting_font(input_reward, reward_rect.width, max_font=16)
            color_reward = CZARNY if input_reward != "0" or active_field == "reward" else JASNY_SZARY
            screen.blit(font_reward.render(input_reward, True, color_reward),
                        (reward_rect.x + 10, reward_rect.y + (reward_rect.height - font_reward.size(input_reward)[1]) // 2))
            counter_surface = counter_font.render(f"Max: {MAX_REWARD}", True, SZARY)
            screen.blit(counter_surface, (reward_rect.right - counter_surface.get_width() - 5,
                                          reward_rect.bottom - counter_surface.get_height() - 5))
            y_offset = reward_rect.bottom + 10

            add_enabled = input_title.strip() != "" and input_title != "Tytuł..."
            add_rect = pygame.Rect(inner_x, y_offset, (form_rect.width - 50)//2, 36)
            cancel_rect = pygame.Rect(add_rect.right + 8, y_offset, (form_rect.width - 50)//2, 36)
            add_color = PRZYCISK_HOVER if add_rect.collidepoint(mouse_pos) else PRZYCISK_BG
            cancel_color = PRZYCISK_HOVER if cancel_rect.collidepoint(mouse_pos) else PRZYCISK_BG
            text_color_add = CZARNY if add_rect.collidepoint(mouse_pos) else BIALY
            text_color_cancel = CZARNY if cancel_rect.collidepoint(mouse_pos) else BIALY
            if not add_enabled:
                add_color = SZARY
                text_color_add = (120, 120, 120)

            pygame.draw.rect(screen, add_color, add_rect, border_radius=8)
            pygame.draw.rect(screen, cancel_color, cancel_rect, border_radius=8)
            add_text = counter_font.render("Dodaj", True, text_color_add)
            cancel_text = counter_font.render("Anuluj", True, text_color_cancel)
            screen.blit(add_text, (add_rect.centerx - add_text.get_width()//2, add_rect.centery - add_text.get_height()//2))
            screen.blit(cancel_text, (cancel_rect.centerx - cancel_text.get_width()//2, cancel_rect.centery - cancel_text.get_height()//2))

        #Szczegoly dla kliknietego zadania na liscie
        if show_details and selected_task:
            s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            s.fill(PRZYCIEMNIENIE)
            screen.blit(s, (0, 0))

            details_rect = pygame.Rect(WIDTH//2 - 150, HEIGHT//2 - 120, 300, 240)
            pygame.draw.rect(screen, BIALY, details_rect, border_radius=12)
            pygame.draw.rect(screen, FIOLET2, details_rect, 3, border_radius=12)

            details_font = pygame.font.Font(font_path, 20)
            title = details_font.render(f"Tytuł: {selected_task[1]}", True, CZARNY)
            reward = details_font.render(f"Punkty: {selected_task[3]}", True, CZARNY)
            date = details_font.render(f"Dodano: {selected_task[4]}", True, CZARNY)
            desc_lines = wrap_text(f"Opis: {selected_task[2]}", details_font, details_rect.width - 40)

            y_offset = details_rect.y + 20
            screen.blit(title, (details_rect.centerx - title.get_width() // 2, y_offset))
            y_offset += title.get_height() + 15

            for line in desc_lines:
                line_surface = details_font.render(line, True, CZARNY)
                screen.blit(line_surface, (details_rect.x + 20, y_offset))
                y_offset += line_surface.get_height() + 3

            status_text = "Ukończone" if selected_task[5] == 1 else "Nieukończone"
            status = details_font.render(f"Status: {status_text}", True, CZARNY)
            screen.blit(status, (details_rect.x + 20, y_offset + 10))
            screen.blit(reward, (details_rect.x + 20, y_offset + 30))
            screen.blit(date, (details_rect.x + 20, y_offset + 50))

            close_font = pygame.font.Font(font_path, 18)
            if selected_task[5] == 0:
                button_width = 100
                button_height = 30
                spacing = 30
                total_width = button_width * 2 + spacing
                start_x = details_rect.centerx - total_width // 2
                done_rect = pygame.Rect(start_x, details_rect.bottom - 40, button_width, button_height)
                close_rect = pygame.Rect(start_x + button_width + spacing, details_rect.bottom - 40, button_width, button_height)

                done_color = ZIELONY if done_rect.collidepoint(mouse_pos) else SZARY
                done_font_color = CZARNY if done_rect.collidepoint(mouse_pos) else BIALY
                close_color = ZIELONY if close_rect.collidepoint(mouse_pos) else SZARY
                close_font_color = CZARNY if close_rect.collidepoint(mouse_pos) else BIALY
                close_text = close_font.render("Zamknij", True, close_font_color)

                pygame.draw.rect(screen, done_color, done_rect, border_radius=8)
                pygame.draw.rect(screen, close_color, close_rect, border_radius=8)
                close_text = close_font.render("Zamknij", True, close_font_color)
                done_text = close_font.render("Wykonane", True, done_font_color)
                screen.blit(done_text, (done_rect.centerx - done_text.get_width() // 2,
                                        done_rect.centery - done_text.get_height() // 2))
                screen.blit(close_text, (close_rect.centerx - close_text.get_width() // 2,
                                         close_rect.centery - close_text.get_height() // 2))
            else:
                close_rect = pygame.Rect(details_rect.centerx - 50, details_rect.bottom - 40, 100, 30)
                close_color = FIOLET2 if close_rect.collidepoint(mouse_pos) else SZARY
                close_text = close_font.render("Zamknij", True, BIALY)
                pygame.draw.rect(screen, close_color, close_rect, border_radius=8)
                screen.blit(close_text, (close_rect.centerx - close_text.get_width() // 2,
                                         close_rect.centery - close_text.get_height() // 2))

    elif active_tab == "Sklep":
        draw_sklep(screen, WIDTH, HEIGHT, font_path, punkty_gracza)
    elif active_tab == "Walka":
        draw_walka(screen, WIDTH, HEIGHT, font_path)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

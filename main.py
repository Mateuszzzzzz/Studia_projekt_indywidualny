import pygame
import sqlite3
import os
from datetime import datetime
from sklep import draw_sklep
from walka import draw_walka

pygame.init()

#Ustawienia okna
WIDTH, HEIGHT = 375, 667
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lista zadań")

#Kolory
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)
FIOLET = (96, 43, 96)
ZIELONY = (81, 206, 49)
SZARY = (150, 150, 150)
FIOLET2 = (200, 191, 231)
PRZYCIEMNIENIE = (0, 0, 0, 150)
PRZYCISK_BG = (180, 180, 180)
PRZYCISK_HOVER = (203, 137, 203)
AKTYWNE_POLE = (0, 255, 0)
PLACEHOLDER_COLOR = (160, 160, 160)
BRAK_TYTULU_COLOR = (255, 0, 0)

#Czcionki
MAX_FONT_SIZE = 28
MIN_FONT_SIZE = 12
font_path = os.path.join(os.path.dirname(__file__), "Czcionka", "VT323-Regular.ttf")

#Baza danych
db_path = os.path.join("baza_danych", "baza_danych.db")
os.makedirs("baza_danych", exist_ok=True)
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS zadania (
    ID_Zadania INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa_zadania TEXT,
    Opis_zadania TEXT,
    Nagroda INTEGER DEFAULT 0,
    Data_dodania TEXT,
    Czy_zaliczone INTEGER DEFAULT 0
)''')
conn.commit()

input_width = int(WIDTH * 0.85)
title_height, desc_height, reward_height = 50, 80, 40
MAX_TITLE_CHARS, MAX_DESC_CHARS, MAX_REWARD = 30, 60, 9999

input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
active_field = None
show_input = False

title_rect = pygame.Rect((WIDTH - input_width)//2, HEIGHT//4 - title_height, input_width, title_height)
desc_rect = pygame.Rect((WIDTH - input_width)//2, title_rect.bottom + 10, input_width, desc_height)
reward_rect = pygame.Rect((WIDTH - input_width)//2, desc_rect.bottom + 10, input_width//2, reward_height)

#Przycisk nwoego zadania
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

#Przyciski dodaj i anuluj
btn_width = int(WIDTH * 0.35)
btn_height = 40
add_rect = pygame.Rect(title_rect.x, reward_rect.bottom + 15, btn_width, btn_height)
cancel_rect = pygame.Rect(title_rect.right - btn_width, reward_rect.bottom + 15, btn_width, btn_height)

#Zakładki
tabs = ["Zadania", "Sklep", "Walka"]
active_tab = "Zadania"
tab_height = 50
tab_width = WIDTH // len(tabs)
tab_font = pygame.font.Font(font_path, 24)

#Funkcje
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
            "font": font
        })
    return tasks_prepared

def add_task_to_db(title, desc, reward):
    if not title.strip() or title == "Tytuł...":
        return
    cur.execute("INSERT INTO zadania (Nazwa_zadania, Opis_zadania, Nagroda, Data_dodania) VALUES (?, ?, ?, ?)",
                (title, desc, reward, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def complete_task(task_id):
    cur.execute("UPDATE zadania SET Czy_zaliczone = 1 WHERE ID_Zadania = ?", (task_id,))
    conn.commit()

tasks = load_tasks()
selected_task = None
show_details = False

#Pygame
running = True
clock = pygame.time.Clock()
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i, tab in enumerate(tabs):
                tab_rect = pygame.Rect(i * tab_width, 0, tab_width, tab_height)
                if tab_rect.collidepoint(event.pos):
                    active_tab = tab
                    show_input = False
                    active_field = None
                    break

            if active_tab == "Zadania":
                if not show_input and button_rect.collidepoint(event.pos) and not show_details:
                    show_input = True
                    active_field = "title"
                    input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"

                if show_input:
                    if title_rect.collidepoint(event.pos):
                        active_field = "title"
                        if input_title == "Tytuł...":
                            input_title = ""
                    elif desc_rect.collidepoint(event.pos):
                        active_field = "desc"
                        if input_desc == "Opis...":
                            input_desc = ""
                    elif reward_rect.collidepoint(event.pos):
                        active_field = "reward"
                        if input_reward == "0":
                            input_reward = ""
                    elif add_rect.collidepoint(event.pos) and input_title.strip() != "" and input_title != "Tytuł...":
                        reward_val = int(input_reward) if input_reward.isdigit() else 0
                        add_task_to_db(input_title, input_desc, reward_val)
                        tasks = load_tasks()
                        input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
                        show_input = False
                        active_field = None
                    elif cancel_rect.collidepoint(event.pos):
                        input_title, input_desc, input_reward = "Tytuł...", "Opis...", "0"
                        show_input = False
                        active_field = None
                    else:
                        if not (title_rect.collidepoint(event.pos) or desc_rect.collidepoint(event.pos) or reward_rect.collidepoint(event.pos)):
                            active_field = None
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
                    if input_title == "" and active_field == "title":
                        pass
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

    screen.fill(FIOLET)

    #Zakładki
    for i, tab in enumerate(tabs):
        tab_rect = pygame.Rect(i * tab_width, 0, tab_width, tab_height)
        if tab == active_tab:
            pygame.draw.rect(screen, FIOLET2, tab_rect)
        elif tab_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, PRZYCISK_HOVER, tab_rect)
        else:
            pygame.draw.rect(screen, PRZYCISK_BG, tab_rect)
        pygame.draw.rect(screen, CZARNY, tab_rect, 2)
        text_surface = tab_font.render(tab, True, CZARNY)
        screen.blit(text_surface, (tab_rect.centerx - text_surface.get_width() // 2,
                                   tab_rect.centery - text_surface.get_height() // 2))

    task_positions = []

    if active_tab == "Zadania":
        y = tab_height + 10
        for task in tasks:
            color = BIALY if task["completed"] else CZARNY
            text_surface = task["font"].render(task["text"], True, color)
            border_rect = pygame.Rect(9, y, WIDTH - 18, 35)
            pygame.draw.rect(screen, ZIELONY, border_rect, border_radius=8) if task["completed"] else pygame.draw.rect(screen, FIOLET2, border_rect, border_radius=8)
            pygame.draw.rect(screen, BIALY, border_rect, width = 2, border_radius=8)
            screen.blit(
                text_surface,
                (
                    18,
                    border_rect.y + 5
                )
            )
            task_positions.append((border_rect, task["id"]))
            y += border_rect.height + 10

        #Przycisk plus
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

            #Tytuł
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
            color_title = CZARNY if input_title != "Tytuł..." or active_field == "title" else PLACEHOLDER_COLOR
            screen.blit(font_title.render(input_title, True, color_title),
                        (title_rect.x + 10, title_rect.y + (title_rect.height - font_title.size(input_title)[1]) // 2))
            counter_surface = counter_font.render(f"{len(input_title)}/{MAX_TITLE_CHARS}", True, SZARY)
            screen.blit(counter_surface, (title_rect.right - counter_surface.get_width() - 5,
                                          title_rect.bottom - counter_surface.get_height() - 5))
            y_offset = title_rect.bottom + 12

            #Opis
            desc_border_color = AKTYWNE_POLE if active_field == "desc" else FIOLET2
            desc_rect = pygame.Rect(inner_x, y_offset, form_rect.width - 40, 80)
            pygame.draw.rect(screen, (245, 245, 245), desc_rect, border_radius=8)
            pygame.draw.rect(screen, desc_border_color, desc_rect, 2, border_radius=8)
            font_desc = get_fitting_font(input_desc, desc_rect.width, max_font=20)
            color_desc = CZARNY if input_desc != "Opis..." or active_field == "desc" else PLACEHOLDER_COLOR

            desc_lines = wrap_text(input_desc, font_desc, desc_rect.width - 15)
            y_text = desc_rect.y + 6
            for line in desc_lines:
                screen.blit(font_desc.render(line, True, color_desc), (desc_rect.x + 8, y_text))
                y_text += font_desc.size(line)[1] + 2

            counter_surface = counter_font.render(f"{len(input_desc)}/{MAX_DESC_CHARS}", True, SZARY)
            screen.blit(counter_surface, (desc_rect.right - counter_surface.get_width() - 5,
                                          desc_rect.bottom - counter_surface.get_height() - 5))
            y_offset = desc_rect.bottom + 10

            #Nagroda
            reward_border_color = AKTYWNE_POLE if active_field == "reward" else FIOLET2
            reward_rect = pygame.Rect(inner_x, y_offset, (form_rect.width - 40)//2, 38)
            pygame.draw.rect(screen, (245, 245, 245), reward_rect, border_radius=8)
            pygame.draw.rect(screen, reward_border_color, reward_rect, 2, border_radius=8)
            font_reward = get_fitting_font(input_reward, reward_rect.width, max_font=16)
            color_reward = CZARNY if input_reward != "0" or active_field == "reward" else PLACEHOLDER_COLOR
            screen.blit(font_reward.render(input_reward, True, color_reward),
                        (reward_rect.x + 10, reward_rect.y + (reward_rect.height - font_reward.size(input_reward)[1]) // 2))
            counter_surface = counter_font.render(f"Max: {MAX_REWARD}", True, SZARY)
            screen.blit(counter_surface, (reward_rect.right - counter_surface.get_width() - 5,
                                          reward_rect.bottom - counter_surface.get_height() - 5))
            y_offset = reward_rect.bottom + 10  # mniejszy odstęp niż wcześniej

            #Przyciski
            add_enabled = input_title.strip() != "" and input_title != "Tytuł..."
            add_rect = pygame.Rect(inner_x, y_offset, (form_rect.width - 50)//2, 36)
            cancel_rect = pygame.Rect(add_rect.right + 20, y_offset, (form_rect.width - 50)//2, 36)
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

        #Szczegóły zadania
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

            # wyśrodkowanie tekstu wewnątrz okna
            y_offset = details_rect.y + 20
            screen.blit(title, (details_rect.centerx - title.get_width() // 2, y_offset))
            y_offset += title.get_height() + 15

            for line in desc_lines:
                line_surface = details_font.render(line, True, CZARNY)
                screen.blit(line_surface, (details_rect.x + 20, y_offset))
                y_offset += line_surface.get_height() + 3

            # Status zadania
            status_text = "Ukończone" if selected_task[5] == 1 else "Nieukończone"
            status = details_font.render(f"Status: {status_text}", True, CZARNY)
            screen.blit(status, (details_rect.x + 20, y_offset + 10))

            # Nagroda
            screen.blit(reward, (details_rect.x + 20, y_offset + 30))
            # Data dodania
            screen.blit(date, (details_rect.x + 20, y_offset + 50))

            # przycisk zamykania i wykonania
            close_font = pygame.font.Font(font_path, 18)
            close_text = close_font.render("Zamknij", True, BIALY)

            # przyciski zamknij i wykonane
            close_font = pygame.font.Font(font_path, 18)
            close_text = close_font.render("Zamknij", True, BIALY)

            if selected_task[5] == 0:
                button_width = 100
                button_height = 30
                spacing = 30
                total_width = button_width * 2 + spacing
                start_x = details_rect.centerx - total_width // 2
                done_rect = pygame.Rect(start_x, details_rect.bottom - 40, button_width, button_height)
                close_rect = pygame.Rect(start_x + button_width + spacing, details_rect.bottom - 40, button_width,
                                         button_height)

                done_color = FIOLET2 if done_rect.collidepoint(mouse_pos) else SZARY
                close_color = FIOLET2 if close_rect.collidepoint(mouse_pos) else SZARY

                pygame.draw.rect(screen, done_color, done_rect, border_radius=8)
                pygame.draw.rect(screen, close_color, close_rect, border_radius=8)

                done_text = close_font.render("Wykonane", True, BIALY)
                screen.blit(done_text, (done_rect.centerx - done_text.get_width() // 2,
                                        done_rect.centery - done_text.get_height() // 2))
                screen.blit(close_text, (close_rect.centerx - close_text.get_width() // 2,
                                         close_rect.centery - close_text.get_height() // 2))
            else:
                close_rect = pygame.Rect(details_rect.centerx - 50, details_rect.bottom - 40, 100, 30)
                close_color = FIOLET2 if close_rect.collidepoint(mouse_pos) else SZARY
                pygame.draw.rect(screen, close_color, close_rect, border_radius=8)
                screen.blit(close_text, (close_rect.centerx - close_text.get_width() // 2,
                                         close_rect.centery - close_text.get_height() // 2))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if selected_task:
                    if selected_task[5] == 0 and done_rect.collidepoint(mouse_pos):
                        complete_task(selected_task[0])
                        tasks = load_tasks()
                        cur.execute("SELECT * FROM zadania WHERE ID_Zadania = ?", (selected_task[0],))
                        selected_task = cur.fetchone()

                    if close_rect.collidepoint(mouse_pos):
                        show_details = False
                        selected_task = None


    elif active_tab == "Sklep":
        draw_sklep(screen, WIDTH, HEIGHT, font_path)
    elif active_tab == "Walka":
        draw_walka(screen, WIDTH, HEIGHT, font_path)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

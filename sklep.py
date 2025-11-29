import pygame
import os
import random

ILE_ITEMOW = 17
ZIELONY = (29, 162, 84)
ZIELONY2 = (39, 46, 42)
CZARNY = (0, 0, 0)

def draw_sklep(screen, WIDTH, HEIGHT, font_path, punkty_gracza, ukonczone_zadania):
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

    #PRZEDMIOTY!!!
    #przedmiot 1
    if not hasattr(draw_sklep, "item1ran"):
        draw_sklep.item1ran = random.randint(1, ILE_ITEMOW)
        if draw_sklep.item1ran < 10:
            draw_sklep.item1num = f"00{draw_sklep.item1ran}"
        elif draw_sklep.item1ran < 100:
            draw_sklep.item1num = f"0{draw_sklep.item1ran}"
        else:
            draw_sklep.item1num = str(draw_sklep.item1ran)

        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item1num}.png")
        draw_sklep.shop_img1 = pygame.image.load(shop_path).convert_alpha()
    screen.blit(draw_sklep.shop_img1, (10, 310))

    #przedmiot 2
    if not hasattr(draw_sklep, "item2ran"):
        draw_sklep.item2ran = random.randint(1, ILE_ITEMOW)
        if draw_sklep.item2ran < 10:
            draw_sklep.item2num = f"00{draw_sklep.item2ran}"
        elif draw_sklep.item2ran < 100:
            draw_sklep.item2num = f"0{draw_sklep.item2ran}"
        else:
            draw_sklep.item2num = str(draw_sklep.item2ran)

        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item2num}.png")
        draw_sklep.shop_img2 = pygame.image.load(shop_path).convert_alpha()
    screen.blit(draw_sklep.shop_img2, (84, 310))

    #przedmiot 3
    if not hasattr(draw_sklep, "item3ran"):
        draw_sklep.item3ran = random.randint(1, ILE_ITEMOW)
        if draw_sklep.item3ran < 10:
            draw_sklep.item3num = f"00{draw_sklep.item3ran}"
        elif draw_sklep.item3ran < 100:
            draw_sklep.item3num = f"0{draw_sklep.item3ran}"
        else:
            draw_sklep.item3num = str(draw_sklep.item3ran)

        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item3num}.png")
        draw_sklep.shop_img3 = pygame.image.load(shop_path).convert_alpha()
    screen.blit(draw_sklep.shop_img3, (158, 310))

    #przedmiot 4
    if not hasattr(draw_sklep, "item4ran"):
        draw_sklep.item4ran = random.randint(1, ILE_ITEMOW)
        if draw_sklep.item4ran < 10:
            draw_sklep.item4num = f"00{draw_sklep.item4ran}"
        elif draw_sklep.item4ran < 100:
            draw_sklep.item4num = f"0{draw_sklep.item4ran}"
        else:
            draw_sklep.item4num = str(draw_sklep.item4ran)

        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item4num}.png")
        draw_sklep.shop_img4 = pygame.image.load(shop_path).convert_alpha()
    screen.blit(draw_sklep.shop_img4, (232, 310))

    #przedmiot 5
    if not hasattr(draw_sklep, "item5ran"):
        draw_sklep.item5ran = random.randint(1, ILE_ITEMOW)
        if draw_sklep.item5ran < 10:
            draw_sklep.item5num = f"00{draw_sklep.item5ran}"
        elif draw_sklep.item5ran < 100:
            draw_sklep.item5num = f"0{draw_sklep.item5ran}"
        else:
            draw_sklep.item5num = str(draw_sklep.item5ran)

        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item5num}.png")
        draw_sklep.shop_img5 = pygame.image.load(shop_path).convert_alpha()
    screen.blit(draw_sklep.shop_img5, (306, 310))

    if ukonczone_zadania >= 10:  #drugi ciag itemow
        #przedmiot 6
        if not hasattr(draw_sklep, "item6ran"):
            draw_sklep.item6ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item6ran < 10:
                draw_sklep.item6num = f"00{draw_sklep.item6ran}"
            elif draw_sklep.item6ran < 100:
                draw_sklep.item6num = f"0{draw_sklep.item6ran}"
            else:
                draw_sklep.item6num = str(draw_sklep.item6ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item6num}.png")
            draw_sklep.shop_img6 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img6, (10, 384))

        #przedmiot 7
        if not hasattr(draw_sklep, "item7ran"):
            draw_sklep.item7ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item7ran < 10:
                draw_sklep.item7num = f"00{draw_sklep.item7ran}"
            elif draw_sklep.item7ran < 100:
                draw_sklep.item7num = f"0{draw_sklep.item7ran}"
            else:
                draw_sklep.item7num = str(draw_sklep.item7ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item7num}.png")
            draw_sklep.shop_img7 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img7, (84, 384))

        #przedmiot 8
        if not hasattr(draw_sklep, "item8ran"):
            draw_sklep.item8ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item8ran < 10:
                draw_sklep.item8num = f"00{draw_sklep.item8ran}"
            elif draw_sklep.item8ran < 100:
                draw_sklep.item8num = f"0{draw_sklep.item8ran}"
            else:
                draw_sklep.item8num = str(draw_sklep.item8ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item8num}.png")
            draw_sklep.shop_img8 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img8, (158, 384))

        #przedmiot 9
        if not hasattr(draw_sklep, "item9ran"):
            draw_sklep.item9ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item9ran < 10:
                draw_sklep.item9num = f"00{draw_sklep.item9ran}"
            elif draw_sklep.item9ran < 100:
                draw_sklep.item9num = f"0{draw_sklep.item9ran}"
            else:
                draw_sklep.item9num = str(draw_sklep.item9ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item9num}.png")
            draw_sklep.shop_img9 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img9, (232, 384))

        #przedmiot 10
        if not hasattr(draw_sklep, "item10ran"):
            draw_sklep.item10ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item10ran < 10:
                draw_sklep.item10num = f"00{draw_sklep.item10ran}"
            elif draw_sklep.item10ran < 100:
                draw_sklep.item10num = f"0{draw_sklep.item10ran}"
            else:
                draw_sklep.item10num = str(draw_sklep.item10ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item10num}.png")
            draw_sklep.shop_img10 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img10, (306, 384))
    else:
        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada1.png")
        draw_sklep.shop_block1 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_block1, (10, 384))

    if ukonczone_zadania >= 20:  #trzeci ciag itemow
        if not hasattr(draw_sklep, "item11ran"):
            draw_sklep.item11ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item11ran < 10:
                draw_sklep.item11num = f"00{draw_sklep.item11ran}"
            elif draw_sklep.item11ran < 100:
                draw_sklep.item11num = f"0{draw_sklep.item11ran}"
            else:
                draw_sklep.item11num = str(draw_sklep.item11ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item11num}.png")
            draw_sklep.shop_img11 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img11, (10, 458))

        if not hasattr(draw_sklep, "item12ran"):
            draw_sklep.item12ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item12ran < 10:
                draw_sklep.item12num = f"00{draw_sklep.item12ran}"
            elif draw_sklep.item12ran < 100:
                draw_sklep.item12num = f"0{draw_sklep.item12ran}"
            else:
                draw_sklep.item12num = str(draw_sklep.item12ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item12num}.png")
            draw_sklep.shop_img12 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img12, (84, 458))

        if not hasattr(draw_sklep, "item13ran"):
            draw_sklep.item13ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item13ran < 10:
                draw_sklep.item13num = f"00{draw_sklep.item13ran}"
            elif draw_sklep.item13ran < 100:
                draw_sklep.item13num = f"0{draw_sklep.item13ran}"
            else:
                draw_sklep.item13num = str(draw_sklep.item13ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item13num}.png")
            draw_sklep.shop_img13 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img13, (158, 458))

        if not hasattr(draw_sklep, "item14ran"):
            draw_sklep.item14ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item14ran < 10:
                draw_sklep.item14num = f"00{draw_sklep.item14ran}"
            elif draw_sklep.item14ran < 100:
                draw_sklep.item14num = f"0{draw_sklep.item14ran}"
            else:
                draw_sklep.item14num = str(draw_sklep.item14ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item14num}.png")
            draw_sklep.shop_img14 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img14, (232, 458))

        if not hasattr(draw_sklep, "item15ran"):
            draw_sklep.item15ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item15ran < 10:
                draw_sklep.item15num = f"00{draw_sklep.item15ran}"
            elif draw_sklep.item15ran < 100:
                draw_sklep.item15num = f"0{draw_sklep.item15ran}"
            else:
                draw_sklep.item15num = str(draw_sklep.item15ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item15num}.png")
            draw_sklep.shop_img15 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img15, (306, 458))
    else:
        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada2.png")
        draw_sklep.shop_block2 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_block2, (10, 458))

    if ukonczone_zadania >= 50:  #czwarty ciag itemow
        if not hasattr(draw_sklep, "item16ran"):
            draw_sklep.item16ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item16ran < 10:
                draw_sklep.item11num = f"00{draw_sklep.item16ran}"
            elif draw_sklep.item16ran < 100:
                draw_sklep.item16num = f"0{draw_sklep.item16ran}"
            else:
                draw_sklep.item16num = str(draw_sklep.item16ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item16num}.png")
            draw_sklep.shop_img16 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img16, (10, 532))

        if not hasattr(draw_sklep, "item17ran"):
            draw_sklep.item17ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item17ran < 10:
                draw_sklep.item17num = f"00{draw_sklep.item17ran}"
            elif draw_sklep.item17ran < 100:
                draw_sklep.item17num = f"0{draw_sklep.item17ran}"
            else:
                draw_sklep.item17num = str(draw_sklep.item17ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item17num}.png")
            draw_sklep.shop_img17 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img17, (84, 532))

        if not hasattr(draw_sklep, "item18ran"):
            draw_sklep.item18ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item18ran < 10:
                draw_sklep.item18num = f"00{draw_sklep.item18ran}"
            elif draw_sklep.item18ran < 100:
                draw_sklep.item18num = f"0{draw_sklep.item18ran}"
            else:
                draw_sklep.item18num = str(draw_sklep.item18ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item18num}.png")
            draw_sklep.shop_img18 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img18, (158, 532))

        if not hasattr(draw_sklep, "item19ran"):
            draw_sklep.item19ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item19ran < 10:
                draw_sklep.item19num = f"00{draw_sklep.item19ran}"
            elif draw_sklep.item19ran < 100:
                draw_sklep.item19num = f"0{draw_sklep.item19ran}"
            else:
                draw_sklep.item19num = str(draw_sklep.item19ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item19num}.png")
            draw_sklep.shop_img19 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img19, (232, 532))

        if not hasattr(draw_sklep, "item20ran"):
            draw_sklep.item20ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item20ran < 10:
                draw_sklep.item20num = f"00{draw_sklep.item20ran}"
            elif draw_sklep.item20ran < 100:
                draw_sklep.item20num = f"0{draw_sklep.item20ran}"
            else:
                draw_sklep.item20num = str(draw_sklep.item20ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item20num}.png")
            draw_sklep.shop_img20 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img20, (306, 532))
    else:
        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada3.png")
        draw_sklep.shop_block3 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_block3, (10, 532))

    if ukonczone_zadania >= 99:  #czwarty ciag itemow
        if not hasattr(draw_sklep, "item21ran"):
            draw_sklep.item21ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item21ran < 10:
                draw_sklep.item21num = f"00{draw_sklep.item21ran}"
            elif draw_sklep.item21ran < 100:
                draw_sklep.item21num = f"0{draw_sklep.item21ran}"
            else:
                draw_sklep.item21num = str(draw_sklep.item21ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item21num}.png")
            draw_sklep.shop_img21 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img21, (10, 606))

        if not hasattr(draw_sklep, "item22ran"):
            draw_sklep.item22ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item22ran < 10:
                draw_sklep.item22num = f"00{draw_sklep.item22ran}"
            elif draw_sklep.item22ran < 100:
                draw_sklep.item22num = f"0{draw_sklep.item22ran}"
            else:
                draw_sklep.item22num = str(draw_sklep.item22ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item22num}.png")
            draw_sklep.shop_img22 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img22, (84, 606))

        if not hasattr(draw_sklep, "item23ran"):
            draw_sklep.item23ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item23ran < 10:
                draw_sklep.item23num = f"00{draw_sklep.item23ran}"
            elif draw_sklep.item23ran < 100:
                draw_sklep.item23num = f"0{draw_sklep.item23ran}"
            else:
                draw_sklep.item23num = str(draw_sklep.item23ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item23num}.png")
            draw_sklep.shop_img23 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img23, (158, 606))

        if not hasattr(draw_sklep, "item19ran"):
            draw_sklep.item24ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item24ran < 10:
                draw_sklep.item24num = f"00{draw_sklep.item24ran}"
            elif draw_sklep.item24ran < 100:
                draw_sklep.item24num = f"0{draw_sklep.item24ran}"
            else:
                draw_sklep.item24num = str(draw_sklep.item24ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item24num}.png")
            draw_sklep.shop_img24 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img24, (232, 606))

        if not hasattr(draw_sklep, "item25ran"):
            draw_sklep.item25ran = random.randint(1, ILE_ITEMOW)
            if draw_sklep.item25ran < 10:
                draw_sklep.item25num = f"00{draw_sklep.item25ran}"
            elif draw_sklep.item25ran < 100:
                draw_sklep.item25num = f"0{draw_sklep.item25ran}"
            else:
                draw_sklep.item25num = str(draw_sklep.item25ran)

            shop_path = os.path.join(os.path.dirname(__file__), "Grafika", f"Item{draw_sklep.item25num}.png")
            draw_sklep.shop_img25 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_img25, (306, 606))
    else:
        shop_path = os.path.join(os.path.dirname(__file__), "Grafika", "Sklep_blokada4.png")
        draw_sklep.shop_block4 = pygame.image.load(shop_path).convert_alpha()
        screen.blit(draw_sklep.shop_block4, (10, 606))



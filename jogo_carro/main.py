import pygame
from random import randint
from pathlib import Path

pygame.mixer.pre_init(44100, -16, 2, 1024)
pygame.init()

# Resolucao
screen_width = 800
screen_height = 600
fps = 120

# Colores
color_black = (0, 0, 0)
color_white = (255, 255, 255)
color_red = (200, 0, 0)
color_green = (0, 200, 0)

# Janela
game_icon = pygame.image.load('data/imgs/icons/icon.png')
pygame.display.set_icon(game_icon)


game_title = ['Super', 'Car', 'Crash']
screen = pygame.display.set_mode((screen_width, screen_height), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption(' '.join(game_title))

# tempo
clock = pygame.time.Clock()

# Fontes
bold_font = 'data/fonts/GothamBold.ttf'
medium_font = 'data/fonts/Roboto-Medium.ttf'
light_font = 'data/fonts/Roboto-Light.ttf'

# opções
speaker_icon = pygame.image.load('data/imgs/icons/speaker.png')
speaker_mute_icon = pygame.image.load('data/imgs/icons/speaker_mute.png')

arrow_icon = pygame.image.load('data/imgs/icons/arrow.png')

help_img = pygame.image.load('data/imgs/help.png')


car1 = pygame.image.load('data/imgs/vehicles/car.png')
car1_width = 80
car1_height = 187

car2 = pygame.image.load('data/imgs/vehicles/audi.png')
car2_width = 80
car2_height = 175

car3 = pygame.image.load('data/imgs/vehicles/taxi.png')
car3_width = 80
car3_height = 156

car4 = pygame.image.load('data/imgs/vehicles/black_viper.png')
car4_width = 80
car4_height = 170

car5 = pygame.image.load('data/imgs/vehicles/mini_truck.png')
car5_width = 80
car5_height = 148

car6 = pygame.image.load('data/imgs/vehicles/mini_van.png')
car6_width = 80
car6_height = 169

car7 = pygame.image.load('data/imgs/vehicles/police.png')
car7_width = 80
car7_height = 175

car8 = pygame.image.load('data/imgs/vehicles/ambulance.png')
car8_width = 80
car8_height = 162

car9 = pygame.image.load('data/imgs/vehicles/truck.png')
car9_width = 80
car9_height = 195

# menu
row1 = 170
row2 = 380

column1 = 60
column2 = 160
column3 = 260
column4 = 360
column5 = 460
column6 = 560
column7 = 660

car1_pos = (column1, row1)
car2_pos = (column2, row1)
car3_pos = (column3, row1)
car4_pos = (column4, row1)
car5_pos = (column5, row1)
car6_pos = (column6, row1)
car7_pos = (column7, row1)
car8_pos = (column1, row2)
car9_pos = (column2, row2)

# Default vehicle
car = car1
car_width = car1_width
car_height = car1_height

car_selected = car1
car_selected_pos = car1_pos

# Som
car_crash_sound = pygame.mixer.Sound('data/sounds/car_crash.wav')
countdown_1_sound = pygame.mixer.Sound('data/sounds/countdown_1.wav')
countdown_2_sound = pygame.mixer.Sound('data/sounds/countdown_2.wav')
button_select = pygame.mixer.Sound('data/sounds/button_select.wav')
button_click = pygame.mixer.Sound('data/sounds/button_click.wav')

# Loop variaveis
paused = crashed = False
menu = game = True

# Outras variaveis
alpha_objective_reached = alpha_loop_completed = music_mute = False
button1_sound = button2_sound = button3_sound = button4_sound = True
highscore = None
button_height = 45


# Funcoes
def quit_game():
    pygame.quit()
    quit()


def event_quit_game(event):
    if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and \
            event.key == pygame.K_F4 and pygame.key.get_mods() & pygame.KMOD_LALT:
        quit_game()


def read_highscore():
    global highscore

    score_savefile = Path('scc_savefile.dat')

    if score_savefile.is_file():
        data = []

        with open('scc_savefile.dat', 'r') as save:
            for c in save.read().split():
                try:
                    data.append(int(c))
                except ValueError:
                    data.clear()
                    break

        if len(data) != 0 and data[0] > 0:
            highscore = data[0]
        else:
            highscore = None

    else:
        highscore = None


def write_highscore(score):
    if highscore is not None:
        if score > highscore:
            with open('scc_savefile.dat', 'w') as save:
                save.write(str(score))

    else:
        with open('scc_savefile.dat', 'w') as save:
            save.write(str(score))


def score_wave_update(score):
    score_bak = score

    for n in range(1, 11):
        score_bak += n

        if score_bak % 10 == 0 and score_bak != 0:
            break

        score_bak = score

    return score_bak


def car_select(mouse_pos, car_name, width, height, car_pos):
    global car_selected, car_selected_pos
    global car, car_width, car_height

    if car_pos[0] + width > mouse_pos[0] > car_pos[0] and car_pos[1] + height > mouse_pos[1] > car_pos[1]:
        pygame.mixer.Sound.play(button_click)
        car_selected = car_name
        car_selected_pos = car_pos

        car = car_name
        car_width = width
        car_height = height


def return_menu(mouse_pos, border_x, border_y):

    width = 64
    height = 53

    x = (screen_width - width) - border_x
    y = (screen_height - height) - border_y

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        pygame.mixer.Sound.play(button_click)
        main_menu()

    screen.blit(arrow_icon, (x, y))


def music_toggle(mouse_pos, border_x, border_y):
    global music_mute

    width = 64
    height = 64

    x = (screen_width - width) - border_x
    y = (screen_height - height) - border_y

    if x + width > mouse_pos[0] > x and y + height > mouse_pos[1] > y:
        music_mute = not music_mute
        pygame.mixer.Sound.play(button_click)

    if not music_mute:
        screen.blit(speaker_icon, (x, y))
        pygame.mixer.music.unpause()
    else:
        screen.blit(speaker_mute_icon, (x, y))
        pygame.mixer.music.pause()


def title_text(text, font_size, divide_y=3.5, divide_x=2.0):
    font = pygame.font.Font(bold_font, font_size)
    text_surf, text_rect = text_objects(text, font, color_black)
    text_rect.center = ((screen_width / divide_x), (screen_height / divide_y))
    screen.blit(text_surf, text_rect)


def regular_text(text, font_size, y):
    font = pygame.font.Font(medium_font, font_size)
    text_surf, text_rect = text_objects(text, font, color_black)
    text_rect.center = ((screen_width / 2), (screen_height / 2) + y)
    screen.blit(text_surf, text_rect)


def button_text(text, x, y, width, height, font_size):
    font = pygame.font.Font(medium_font, font_size)
    text_surf, text_rect = text_objects(text, font, color_white)
    text_rect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(text_surf, text_rect)


def creator_text():
    font_size = 15
    border = 20
    x = border
    y = font_size + border

    font = pygame.font.Font(light_font, font_size)
    text = font.render('© 2022 Deboleto ;)', True, color_black)
    screen.blit(text, (x, screen_height - y))


def alpha(color, alpha_channel=200):
    surface = pygame.Surface((screen_width, screen_height), pygame.HWSURFACE)
    surface.set_alpha(alpha_channel)
    surface.fill(color)
    screen.blit(surface, (0, 0))


def alpha_fade(surface, alpha_objective):
    global alpha_objective_reached
    global alpha_loop_completed

    alpha_channel = surface.get_alpha()

    if not alpha_objective_reached and not alpha_loop_completed:
        alpha_channel += 3

        if alpha_channel == 255:
            alpha_objective_reached = True

    elif alpha_objective_reached:
        alpha_channel -= 3

        if alpha_channel == alpha_objective:
            alpha_objective_reached = False
            alpha_loop_completed = True

    return alpha_channel


def random_object_x_pos(object_width):
    return randint(0, screen_width - object_width)


def random_color():
    while True:
        color = (randint(0, 255), randint(0, 255), randint(0, 255))

        if color[0] != color[1] or color[1] != color[2] or color[0] != color[2]:
            if color[0] < 250 and color[1] < 250 and color[2] < 250:
                break

    return color


def show_score(score):
    font = pygame.font.Font(light_font, 25)
    text_surf, text_rect = text_objects(str(score), font, color_black)
    text_rect.center = ((screen_width / 2), 30)
    screen.blit(text_surf, text_rect)


def show_highscore():
    font = pygame.font.Font(light_font, 30)
    text_surf, text_rect = text_objects('Pontuacao: ' + str(highscore), font, color_black)
    text_rect.center = ((screen_width / 2), (screen_height / 3))
    screen.blit(text_surf, text_rect)


def objects(x, y, width, height, color, amount):
    for o in range(0, amount):
        pygame.draw.rect(screen, color, [x[o], y, width, height])
        if amount != 1:
            while True:
                gen_x_pos = random_object_x_pos(width)
                if gen_x_pos > x[o] + width or gen_x_pos + width < x[o]:
                    x.append(gen_x_pos)
                    break


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def button1(mouse_pos, text, y, x=None, action=None, colour=color_green, font_size=20, width=None):
    global button1_sound

    # Mouse status
    mouse_pos_over = pygame.mouse.get_pos()

    # parametros
    if action is None:
        action = text.lower()

    if width is None:
        width = len(text) * (font_size / 2) + 60

    if x is None:
        x = (screen_width / 2) - (width / 2)

    # Cores
    active_colour = []
    for c in colour:
        if c > 50:
            active_colour.append(c - 50)
        else:
            active_colour.append(0)

    # Mouse
    if x + width > mouse_pos_over[0] > x and y + button_height > mouse_pos_over[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, button_height))

        # Botao seleção
        if button1_sound:
            pygame.mixer.Sound.play(button_select)
            button1_sound = False

    else:
        pygame.draw.rect(screen, colour, (x, y, width, button_height))
        button1_sound = True

    # Botao
    if x + width > mouse_pos[0] > x and y + button_height > mouse_pos[1] > y:
        pygame.mixer.Sound.play(button_click)

        # Click acao
        if action == 'play' or action == 'retornar':
            game_loop()
        if action == 'continuar':
            unpause()

    button_text(text, x, y, width, button_height, font_size)


def button2(mouse_pos, text, y, x=None, colour=color_green, action=None, font_size=20, width=None):
    global button2_sound

    # Mouse status
    mouse_pos_over = pygame.mouse.get_pos()


    if action is None:
        action = text.lower()

    if width is None:
        width = len(text) * (font_size / 2) + 60

    if x is None:
        x = (screen_width / 2) - (width / 2)

    # Cores
    active_colour = []
    for c in colour:
        if c > 50:
            active_colour.append(c - 50)
        else:
            active_colour.append(0)

    # botoes mouse
    if x + width > mouse_pos_over[0] > x and y + button_height > mouse_pos_over[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, button_height))

        # Botao seleção
        if button2_sound:
            pygame.mixer.Sound.play(button_select)
            button2_sound = False

    else:
        pygame.draw.rect(screen, colour, (x, y, width, button_height))
        button2_sound = True

    # Botão click
    if x + width > mouse_pos[0] > x and y + button_height > mouse_pos[1] > y:
        pygame.mixer.Sound.play(button_click)

        # Click
        if action == 'Menu':
            pygame.mixer.music.stop()
            main_menu()
        if action == 'carros':
            car_menu()

    button_text(text, x, y, width, button_height, font_size)


def button3(mouse_pos, text, y, x=None, colour=color_green, action=None, font_size=20, width=None):
    global button3_sound

    # Mouse status
    mouse_pos_over = pygame.mouse.get_pos()

    # parametros
    if action is None:
        action = text.lower()

    if width is None:
        width = len(text) * (font_size / 2) + 60

    if x is None:
        x = (screen_width / 2) - (width / 2)


    active_colour = []
    for c in colour:
        if c > 50:
            active_colour.append(c - 50)
        else:
            active_colour.append(0)


    if x + width > mouse_pos_over[0] > x and y + button_height > mouse_pos_over[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, button_height))

        # Botao selecao
        if button3_sound:
            pygame.mixer.Sound.play(button_select)
            button3_sound = False

    else:
        pygame.draw.rect(screen, colour, (x, y, width, button_height))
        button3_sound = True

    # Botao click
    if x + width > mouse_pos[0] > x and y + button_height > mouse_pos[1] > y:
        pygame.mixer.Sound.play(button_click)

        # Click acao
        if action == 'help':
            help_menu()

    button_text(text, x, y, width, button_height, font_size)


def button4(mouse_pos, text, y, x=None, colour=color_red, action=None, font_size=20, width=None):
    global button4_sound

    # Mouse status
    mouse_pos_over = pygame.mouse.get_pos()


    if action is None:
        action = text.lower()

    if width is None:
        width = len(text) * (font_size / 2) + 60

    if x is None:
        x = (screen_width / 2) - (width / 2)


    active_colour = []
    for c in colour:
        if c > 50:
            active_colour.append(c - 50)
        else:
            active_colour.append(0)

    # Mouse over the button
    if x + width > mouse_pos_over[0] > x and y + button_height > mouse_pos_over[1] > y:
        pygame.draw.rect(screen, active_colour, (x, y, width, button_height))

        # Button select
        if button4_sound:
            pygame.mixer.Sound.play(button_select)
            button4_sound = False

    else:
        pygame.draw.rect(screen, colour, (x, y, width, button_height))
        button4_sound = True


    if x + width > mouse_pos[0] > x and y + button_height > mouse_pos[1] > y:
        pygame.mixer.Sound.play(button_click)


        if action == 'Sair':
            quit_game()

    button_text(text, x, y, width, button_height, font_size)


def crash(score):

    # Musica
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(car_crash_sound)

    # Screen display
    alpha(color_white)
    show_score(score)
    title_text('GAME OVER', 50)

    write_highscore(score)

    while crashed:
        mouse_pos = (0, 0)


        for event in pygame.event.get():

            # Sair
            event_quit_game(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()

        # BOTOES
        button1(mouse_pos, 'RETORNAR', 300)
        button2(mouse_pos, 'MENU', 380)
        button4(mouse_pos, 'SAIR', 460)


        pygame.display.flip()
        clock.tick(15)


def pause(score):

    # Musica
    pygame.mixer.music.pause()


    alpha(color_white)
    show_score(score)
    title_text('PAUSAR', 50)

    while paused:
        mouse_pos = (0, 0)


        for event in pygame.event.get():

            # SAIR
            event_quit_game(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()


            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    unpause()

        # BOTOES
        button1(mouse_pos, 'CONTINUAR', 300)
        button2(mouse_pos, 'MENU', 380)
        button4(mouse_pos, 'SAIR', 460)

        # Screen update
        pygame.display.flip()
        clock.tick(15)


def unpause():
    global paused


    pygame.mixer.music.unpause()

    paused = False


def main_menu():
    read_highscore()


    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.load('data/sounds/intro_music.mp3')
        pygame.mixer.music.play(-1)

    # Objetos variaveis
    object_speed = 5
    object_width = 80
    object_height = 80
    object_x = [random_object_x_pos(object_width)]
    object_y = -(object_height * 5)
    object_amount = randint(1, 3)
    object_boost = 0
    object_color = random_color()
    object_count = 0

    while menu:
        mouse_pos = (0, 0)


        for event in pygame.event.get():

            # sair
            event_quit_game(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()


        screen.fill(color_white)

        objects(object_x, object_y, object_width, object_height, object_color, object_amount)

        object_y += object_speed + object_boost


        if object_y > screen_height:
            object_y = 0 - object_height
            object_x.clear()
            object_x.append(random_object_x_pos(object_width))
            object_count += 1
            object_amount = randint(1, 3)

            if object_count % 10 == 0:
                object_color = random_color()

        if highscore is not None:
            show_highscore()

        alpha(color_white)

        title_text(game_title[0].upper(), 80, screen_width / 100 - 2, screen_height / 100 - 4)
        title_text(' '.join(game_title[1:]).upper(), 45, screen_width / 100 - 4, screen_height / 100 - 4)

        creator_text()

        #   Botoes
        button1(mouse_pos, 'PLAY', 270)
        button2(mouse_pos, 'CARROS', 330)
        button3(mouse_pos, 'AJUDA', 390)
        button4(mouse_pos, 'SAIR', 450)

        music_toggle(mouse_pos, 50, 50)


        pygame.display.flip()
        clock.tick(60)


def car_menu():

    while menu:
        mouse_pos = (0, 0)


        for event in pygame.event.get():


            event_quit_game(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()


        screen.fill(color_white)

        # Carros
        screen.blit(car1, car1_pos)
        car_select(mouse_pos, car1, car1_width, car1_height, car1_pos)
        screen.blit(car2, car2_pos)
        car_select(mouse_pos, car2, car2_width, car2_height, car2_pos)
        screen.blit(car3, car3_pos)
        car_select(mouse_pos, car3, car3_width, car3_height, car3_pos)
        screen.blit(car4, car4_pos)
        car_select(mouse_pos, car4, car4_width, car4_height, car4_pos)
        screen.blit(car5, car5_pos)
        car_select(mouse_pos, car5, car5_width, car5_height, car5_pos)
        screen.blit(car6, car6_pos)
        car_select(mouse_pos, car6, car6_width, car6_height, car6_pos)
        screen.blit(car7, car7_pos)
        car_select(mouse_pos, car7, car7_width, car7_height, car7_pos)
        screen.blit(car8, car8_pos)
        car_select(mouse_pos, car8, car8_width, car8_height, car8_pos)
        screen.blit(car9, car9_pos)
        car_select(mouse_pos, car9, car9_width, car9_height, car9_pos)

        alpha(color_white)

        screen.blit(car_selected, car_selected_pos)

        title_text('ESCOLHER UM CARRO', 50, 7)


        return_menu(mouse_pos, 50, 55.5)


        pygame.display.flip()
        clock.tick(15)


def help_menu():

    while menu:
        mouse_pos = (0, 0)

        # Eventos
        for event in pygame.event.get():


            event_quit_game(event)

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = pygame.mouse.get_pos()


        screen.fill(color_white)

        title_text('AJUDA', 50, 7)

        screen.blit(help_img, (75, 150))

        # Botoes
        return_menu(mouse_pos, 50, 55.5)

        # Screen update
        pygame.display.flip()
        clock.tick(15)


def game_loop():
    global paused
    global crashed
    global alpha_objective_reached
    global alpha_loop_completed

    read_highscore()


    if not music_mute:
        pygame.mixer.music.fadeout(50)

    pygame.mixer.music.load('data/sounds/car_start.wav')
    pygame.mixer.music.play()

    # Variaveis
    score = countdown_y = 0
    object_update = score_wave_update(score)
    num_float = message = 3
    alpha_objective_reached = countdown_end = countdown_go = False
    score_boost = []

    #   Carro
    car_x = (screen_width * 0.445)
    car_y = (screen_height * 0.65)
    car_x_change = 0

    #   Objeto
    object_speed = 3
    object_width = 80
    object_height = 80
    object_x = [random_object_x_pos(object_width)]
    object_y = -(object_height * 2)
    object_amount = 1
    object_boost = 0
    object_super_boost = object_super_boost_limit = 0
    object_color = random_color()


    border = pygame.Surface((10, screen_height), pygame.HWSURFACE)
    border.set_alpha(0)

    # Game loop
    while game:


        screen.fill(color_white)

        if not countdown_end or countdown_go:
            if num_float == 0 or num_float == 1 or num_float == 2 or num_float == 3:
                if num_float != 0:
                    message = int(num_float)
                    pygame.mixer.Sound.play(countdown_1_sound)
                    border.fill(color_red)
                    alpha_loop_completed = False
                else:
                    message = 'GO!'
                    pygame.mixer.Sound.play(countdown_2_sound)
                    border.fill(color_green)
                    alpha_loop_completed = False
            if num_float >= -5:
                regular_text(str(message), 50, countdown_y)
                countdown_go = True
            if num_float == -1:
                countdown_end = True
            num_float -= 1 / 128

        screen.blit(border, (0, 0))
        border.set_alpha(alpha_fade(border, 0))

        screen.blit(border, (screen_width - 10, 0))
        border.set_alpha(alpha_fade(border, 0))

        objects(object_x, object_y, object_width, object_height, object_color, object_amount)

        screen.blit(car, (car_x, car_y))

        if score >= 1:
            show_score(score)

        # Event handling
        for event in pygame.event.get():

            # Quit
            event_quit_game(event)

            # Keyboard key down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    car_x_change += -7
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    car_x_change += 7

                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    object_boost = 1 / 4
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    object_boost = -1 / 4

                if event.key == pygame.K_SPACE:
                    object_super_boost = True

                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    paused = True
                    pause(score)


            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    car_x_change += 7
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    car_x_change += -7

                if event.key == pygame.K_UP or event.key == pygame.K_w or \
                        event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    object_boost = 0

        # Carro movimento
        car_x += car_x_change


        if countdown_end:
            object_y += object_speed + object_boost
            countdown_y += object_speed + object_boost
            if object_super_boost:
                object_y += 15
                countdown_y += 15


        if car_x > screen_width - car_width or car_x < 0:
            crashed = True
            crash(score)

        #   Objeto colidir
        if car_y < object_y + object_height and car_y + car_height > object_y:
            for n in range(0, object_amount):
                if object_x[n] < car_x + car_width and object_x[n] + object_width > car_x:
                    crashed = True
                    crash(score)
                else:
                    if object_boost > 4:
                        score_boost.append(True)
                    else:
                        score_boost.append(False)

        # objetos
        if object_y > screen_height:
            countdown_go = False
            object_y = 0 - object_height
            object_x.clear()
            object_x.append(random_object_x_pos(object_width))

            if True not in score_boost:
                score += 1
            else:
                score += 2

            score_boost.clear()

            if score >= object_update:
                object_update = score_wave_update(score)
                object_speed += 1
                object_color = random_color()

            if score % 5 == 0 or score % 4 == 0:
                object_amount = randint(1, 3)


        if object_super_boost:
            object_super_boost_limit += 1

        if object_super_boost_limit == 10:
            object_super_boost = False
            object_super_boost_limit = 0


        if object_boost > 0:
            if object_boost < 5:
                object_boost += 1 / 8

        elif object_boost < 0:
            if object_boost > -2:
                object_boost -= 1 / 8


        pygame.display.flip()
        clock.tick(fps)


main_menu()
quit_game()

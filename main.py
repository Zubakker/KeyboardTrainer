import pygame
import sys
from time import time, sleep
from random import choice

from CONFIG import *


def next_char():
    global TEXT, to_press, word_start, time_spent, begining
    to_press += 1
    """
    if TEXT[to_press - 1] == " ":
        for i in range(word_start, to_press):
            logs.write(TEXT[i])
        for item in time_spent:
            logs.write(" " + str(item))
        logs.write("\n")
        time_spent = []
        word_start = to_press - 1
    """
    if to_press == len(TEXT) - 1:
        """
        for i in range(word_start, to_press):
            logs.write(TEXT[i])
        for item in time_spent:
            logs.write(" " + str(item))
        logs.write("\n")
        """
        logs.close()
        pygame.quit()
        print("  Thank you! Your average cpm was " + str(60* to_press / (time() - begining))[:5])
        print("  And your mistakes rate was", str(100* mistakes / (to_press + 1))[:5] + "%")
        sys.exit()
    return

def gen_text(LETTERS, WORD_LEN, LIMIT):
    TEXT = ""
    for i in range(LIMIT):
        word = ""
        for j in range(WORD_LEN):
            word += choice(LETTERS)
        TEXT += word + " " 
    to_press = 0
    time_spent = list() 
    return TEXT


screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(BG_COLOR)
logs = open("keyboard.log", "a+")
pygame.font.init()
myfont = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

TEXT = ""
to_press = 0 
unpressed = ""
pressed = ""

mistakes = 0
time_spent = list() 
first_press = True
time_pressed = dict()
time_unpressed = time() 
word_start = 0
begining = 0
TEXT = gen_text(LETTERS, WORD_LEN, LIMIT)

f = open("statistics.txt", "a+")

while True:
    # print("kadr", end=" ", flush=True)
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and \
                event.key != pygame.K_LSHIFT and \
                event.key != pygame.K_RSHIFT:
            if first_press:
                first_press = False
                begining = time()
            key = pygame.key.name(event.key)
            """
            if pygame.key.get_pressed()[pygame.K_LSHIFT] or \
                    pygame.key.get_pressed()[pygame.K_RSHIFT]:
                key = "S_" + key
            pressed = LAYOUT[key]
            """
            pressed = key
            if key == "space":
                pressed = " "

            if pressed and TEXT[to_press] == pressed:
                next_char()
            elif pressed != TEXT[to_press]:
                mistakes += 1

            time_pressed[event.key] = time()
            logs.write(str(["xx", time() - time_unpressed]))
            # time_spent.append(("xx", time() - time_unpressed))

        elif event.type == pygame.KEYUP:
            if event.key != pygame.K_LSHIFT and \
                    event.key != pygame.K_RSHIFT:
                if event.key not in list(time_pressed):
                    continue
                logs.write(str([pygame.key.name(event.key), time() - time_pressed[event.key]]))
                # time_spent.append((pygame.key.name(event.key), time() - time_pressed[event.key]))
                time_unpressed = time()
                key = pygame.key.name(event.key)
                if key == "space":
                    key = " "
                unpressed = key
                if pressed == key: #LAYOUT[key]:
                    pressed = ""
    """        
    if unpressed and TEXT[to_press] == unpressed:
        next_char()
    if pressed and TEXT[to_press] == pressed:
        next_char()
    elif unpressed and not pressed and TEXT[to_press] != unpressed:
        mistakes += 1
    """

    pygame.draw.line(screen, UNTYPED_COLOR, (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 - 10), 
            (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2 + 20), 1)

    cpm = myfont.render("CPM: " + str(60* to_press / (time() - begining))[:5], 1, UNTYPED_COLOR)
    screen.blit(cpm, (0, 0))

    cpm = myfont.render("MIS: " + str(100* mistakes / (to_press + 1))[:5] + "%", 1, UNTYPED_COLOR)
    screen.blit(cpm, (0, FONT_SIZE + 5))

    typed = myfont.render(TEXT[:to_press], 1, TYPED_COLOR)
    typed_width = myfont.size(TEXT[:to_press])[0]
    screen.blit(typed, (SCREEN_SIZE[0]//2 - typed_width, SCREEN_SIZE[1]//2))

    untyped = myfont.render(TEXT[to_press:], 1, UNTYPED_COLOR)
    screen.blit(untyped, (SCREEN_SIZE[0]//2, SCREEN_SIZE[1]//2))

    pygame.display.update()
    # sleep(0.01)

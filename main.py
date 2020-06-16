import pygame
import sys
from time import time, sleep
from random import choice

from CONFIG import *


def next_char():
    global TEXT, to_press, word_start, time_spent, begining, stats
    to_press += 1
    if TEXT[to_press] == "|":
        pause()
    if to_press == len(TEXT) - 1:
        logs.close()
        pygame.quit()
        print("  Thank you! Your average cpm was " + str(60* to_press / (time() - begining))[:5])
        print("  And your mistakes rate was", str(100* mistakes / (to_press + 1))[:5] + "%")

        stats.write(str(begining) + "|" + str(len(TEXT)) + "|" + str(time()-begining) + "|" + str(mistakes) + "|" + str(60* to_press / (time() - begining))[:5])
        sys.exit()
    return

def gen_text(LETTERS, WORD_LEN, LIMIT):
    TEXT = ""
    for i in range(LIMIT):
        word = ""
        for j in range(WORD_LEN):
            word += choice(LETTERS)
        TEXT += word + " " 
    time_spent = list() 
    return TEXT


def pause():
    global screen, myfont
    sleep(2)
    txt = myfont.render("Press any button to continue", 1, TYPED_COLOR)
    screen.blit(text, (SCREEN_SIZE//2, 10))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("You stopped at", to_press)
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return


screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(BG_COLOR)
logs = open("keyboard.log", "a+")
pygame.font.init()
myfont = pygame.font.SysFont(FONT_NAME, FONT_SIZE)

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

stats = open("statistics.txt", "a+")

while True:
    # print("kadr", end=" ", flush=True)
    screen.fill(BG_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print("The place you stopped is", to_press)
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and \
                event.key != pygame.K_LSHIFT and \
                event.key != pygame.K_RSHIFT:
            if first_press:
                first_press = False
                begining = time()
            key = pygame.key.name(event.key)
            pressed = key
            if key == "space":
                pressed = " "
            if key == "right alt":
                next_char()
                continue

            if pressed and TEXT[to_press] == pressed:
                next_char()
            elif pressed != TEXT[to_press]:
                mistakes += 1

            time_pressed[event.key] = time()
            logs.write(str(["xx", time() - time_unpressed]))

        elif event.type == pygame.KEYUP:
            if event.key != pygame.K_LSHIFT and \
                    event.key != pygame.K_RSHIFT:
                if event.key not in list(time_pressed):
                    continue
                logs.write(str([pygame.key.name(event.key), time() - time_pressed[event.key]]))
                time_unpressed = time()
                key = pygame.key.name(event.key)
                if key == "space":
                    key = " "
                unpressed = key
                if pressed == key: #LAYOUT[key]:
                    pressed = ""

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

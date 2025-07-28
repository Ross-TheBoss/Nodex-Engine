from engine import * 
import pygame

ctx = Context((1280, 720))

@ctx.loop()
def game_loop():
    for event in ctx.events:
        if event.type == KEYDOWN:
            print(event.key)
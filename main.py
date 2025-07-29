from engine import * 
import pygame

ctx = Context((1280, 720))

root = Node(ctx, "Root")
menu = Node(ctx, "Menu")
game = Node(ctx, "Game")
tilemap = Node(ctx, "Tilemap")
background = Node(ctx, "Background")
player = Node(ctx, "Player")
camera = Node(ctx, "Camera")

background.order = 0
tilemap.order = 1
player.order = 2 

root.link(menu) 
root.link(game)

game.link(tilemap)
game.link(player)

player.link(camera)

for i in range(10):
    tilemap.link(Node(ctx, f'Tile'))
    
print("# INITIAL TREE #")
root.debug()

tlm = tilemap.serialize()
tilemap.unlink()

print()
print("# AFTER REMOVAL #")
root.debug()
print(tlm)
root.search(tlm["pid"]).link(Node.build(tlm))
print()
print("# END #")
root.debug()



import nodex

context = nodex.Context((500, 500), backend="pygame")
texture = context.load_texture("bird.png")

@context.loop()
def game_loop():
    context.draw(texture, (0, 0))
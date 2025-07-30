import nodex 
import random



ctx = nodex.Context((500, 500), backend="pygame")
ball_image = ctx.load_texture("ball.png")

class MovingBird(nodex.Node):
    def __init__(self, context):
        super().__init__(context, "Ball")
        self.x = random.randint(0, 500)
        self.y = random.randint(0, 500)
        self.vx = random.randint(-10, 10)
        self.vy = random.randint(-10, 10)
    
    def update(self):
        self.context.draw(ball_image, (self.x, self.y))
        self.x += self.vx * self.context.dt 
        self.y += self.vy * self.context.dt
        if self.x > 500 or self.x < 0:
            self.vx *= -1
        if self.y > 500 or self.y < 0:
            self.vy *= -1
        
        
        
root = nodex.Node(ctx, "Root")
for i in range(500):
    root.link(MovingBird(ctx))
        
@ctx.loop()
def game_loop():
    ctx.window.set_caption('Nodex Engine | FPS : ' + str(round(ctx.fps, 1)))
    root.update_all()
import nodex

ctx = nodex.Context((1280, 720))

class Player(nodex.Node):
    def __init__(self, position, context):
        super().__init__(context, "Player")
        self.x, self.y = position
        self.debug_info = {"x" : self.x, "y" : self.y}
        self.content["position"] = (self.x, self.y)
    
    def new_root(data):
        player = Player((0, 0), data["context"])
        player.x, player.y = data["position"]
        return player
    
    
p = Player((10, 10), ctx)
print(p)
save = p.serialize()
p_copy = nodex.Node.build(save)
print(p_copy)
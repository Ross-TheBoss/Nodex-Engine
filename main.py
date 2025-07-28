from engine import * 
import pygame

ctx = Context((1280, 720))

class TNode(Node):
    def on_signal(self, content, source):
        super().on_signal(content, source)
        return None

root = Node(ctx, "root")
child1 = Node(ctx, "child1")
child2 = TNode(ctx, "child2")
child3 = Node(ctx, "child3")
gchild1 = Node(ctx, "gchild1")
gchild2 = Node(ctx, "gchild2")
gchild3 = Node(ctx, "gchild3")
gchild4 = Node(ctx, "gchild4")
gchild5 = Node(ctx, "gchild5")
gchild6 = Node(ctx, "gchild6")
gchild7 = Node(ctx, "gchild7")

root.link(child1)
root.link(child2)
root.link(child3)

child1.link(gchild1)
child1.link(gchild2)

child2.link(gchild3)
child2.link(gchild4)
child2.link(gchild5)

child3.link(gchild4)
child3.link(gchild5)
child3.link(gchild6)

root.message("BLABLA")
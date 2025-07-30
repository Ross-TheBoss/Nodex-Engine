from nodex.context.context import *
from typing import *

class Node:
    _id_counter = 0
        
    def __init__(self, context: Context, label: str = "Node"):
        self.context: Context = context
        self.label: str = label
        self.update_: bool = True
        self.children: List["Node"] = []
        self.tags: Set[str] = set({"@" + label})
        self.parent: "Node" | None = None
        self.order: int = 0
        self.id: int = Node._id_counter
        Node._id_counter += 1
        self.content = {}
        self.debug_info = {}

    def _tag_filter(self, element: "Node", tags: Set[str], ignore: Set[str]) -> bool:
        return all(tag in element.tags for tag in tags) and not any(tag in element.tags for tag in ignore)

    def __children_sort(self):
        self.children.sort(key=lambda child: child.order, reverse=True)

    @property
    def root(self) -> "Node":
        return self.parent.root if self.parent is not None else self

    def link(self, child: "Node"):
        self.children.append(child)
        child.parent = self

    def unlink(self):
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def update(self):
        pass
    
    def serialize(self):
        data = dict(self.content) 
        data["type"] = self.__class__.__name__
        data["label"] = self.label
        data["context"] = self.context
        data["init"] = ""
        if self.parent:
            data["pid"] = self.parent.id
        else:
            data["pid"] = -1
        data["children"] = [child.serialize() for child in self.children]
        return data
    
    @staticmethod
    def build(data:dict) -> "Node":
        type_map = {cls.__name__: cls for cls in _all_subclasses(Node)}
        type_map["Node"] = Node
        node = type_map[data["type"]].new_root(data)
        node.children = [Node.build(child) for child in data["children"]]
        return node
    
    def new_root(data:dict) -> "Node":
        return Node(data["context"], data["label"])
    
    def search(self, id):
        if self.id == id:
            return self
        for child in self.children:
            result = child.search(id)
            if result:
                return result
        return None

    def on_message(self, type: str, content: dict, source: "Node") -> Optional[bool]:
        return True

    def update_all(self):
        if self.update_:
            self.update()
            self.__children_sort()
            for child in self.children:
                child.update_all()

    def get_descendants(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List["Node"]:
        output = []

        def recursive_search(node: "Node"):
            node.__children_sort()
            for child in node.children:
                if self._tag_filter(child, tags, ignore):
                    output.append(child)
                recursive_search(child)

        recursive_search(self)
        return output

    def get_ancestors(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List["Node"]:
        output = []

        def recursive_search(node: "Node"):
            if self._tag_filter(node, tags, ignore):
                output.append(node)
            if node.parent is not None:
                recursive_search(node.parent)

        if self.parent is not None:
            recursive_search(self.parent)
        return output

    def get_siblings(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List["Node"]:
        return list(
            filter(
                lambda element: self._tag_filter(element, tags, ignore),
                self.parent.children
            )
        )

    def __repr__(self):
        return f'<{self.label} #{self.id}' + "".join([f' {key} = {value}' for key, value in self.debug_info.items()]) + '>' 

    def debug(self, spaces: int = 4):
        def recursive_helper(node: "Node", level: int):
            if not node.children:
                print(" " * (level * spaces) + node.__repr__()[:-1] + "/>")
            else:
                print(" " * (level * spaces) + node.__repr__())
                for child in node.children:
                    recursive_helper(child, level + 1)
                print(" " * (level * spaces) + node.__repr__()[:-1] + "/>")

        recursive_helper(self, 0)

    def message(self, type: str, content: dict = {}, _source: "Node" = None) -> bool:
        if _source is None:
            _source = self
        self.__children_sort()
        for child in self.children:
            result = child.on_message(type, content, _source)
            if result is False:
                return False
            elif result is True:
                if child.message(type, content, _source) is False:
                    return False
            elif result is None:
                continue
        return True

def _all_subclasses(cls):
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(_all_subclasses(subclass))
    return subclasses


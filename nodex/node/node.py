from nodex.context.context import *
from typing import *

class Node:
    """
    Nodes are hierarchical elements used to organize all aspects of the game.
    """
    
    _id_counter = 0
        
    def __init__(self, context: Context, label: str = "Node"):
        """
        Initializes a new Node.

        Args:
            context (Context): The game context to which the node belongs.
            label (str, optional): The name of the node. Defaults to "Node".
        """
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
        """
        Returns the root node of the hierarchy.
        """
        return self.parent.root if self.parent is not None else self

    def link(self, child: "Node"):
        """
        Adds a child node to this node.

        Args:
            child (Node): The child node to add.
        """
        self.children.append(child)
        child.parent = self

    def unlink(self):
        """
        Detaches this node from its parent.
        """
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def update(self):
        """
        Called when the node is updated. Override this method in subclasses.
        """
        pass
    
    def serialize(self):
        """
        Serializes this node and its subtree into a dictionary for saving.

        Returns:
            dict: A dictionary representation of this node and its children.
        """
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
        _type_map = {cls.__name__: cls for cls in _all_subclasses(Node)}
        _type_map["Node"] = Node
        """ 
        Build a new node from serialized data.
        
        Args:
            data (dict): The dictionary containing serialized node data.
            
        Returns:
            Node: The reconstructed node instance with its full subtree.
        """
        node = _type_map[data["type"]].new_root(data)
        node.children = [Node.build(child) for child in data["children"]]
        return node
    
    def new_root(data:dict) -> "Node":
        """ 
        Create the root of the node we are trying to build.
        
        Args:
            data (dict): The dictionary containing serialized node data.
        """
        return Node(data["context"], data["label"])
    
    def search(self, id):
        """
        Searches recursively in the subtree for a node with a given ID.

        Args:
            id (int): The ID to search for.

        Returns:
            Node | None: The node with the matching ID, or None if not found.
        """
        if self.id == id:
            return self
        for child in self.children:
            result = child.search(id)
            if result:
                return result
        return None

    def on_message(self, type: str, content: dict, source: "Node") -> Optional[bool]:
        """
        Called when the node receives a message.

        Args:
            type (str): The type of the message.
            content (dict): The message content.
            source (Node): The original emitter of the message.

        Returns:
            True: Continue propagating the message.
            False: Stop propagation completely.
            None: Do not propagate to children of this node, but continue otherwise.
        """
        return True

    def update_all(self):
        """
        Updates this node and all its children recursively.
        """
        if self.update_:
            self.update()
            self.__children_sort()
            for child in self.children:
                child.update_all()

    def get_descendants(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List["Node"]:
        """
        Returns all descendant nodes that match the given tag filters.

        Args:
            tags (Set[str], optional): Required tags.
            ignore (Set[str], optional): Tags to exclude.

        Returns:
            List[Node]: The matching descendant nodes.
        """
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
        """
        Returns all ancestor nodes that match the given tag filters.

        Args:
            tags (Set[str], optional): Required tags.
            ignore (Set[str], optional): Tags to exclude.

        Returns:
            List[Node]: The matching ancestor nodes.
        """
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
        """
        Returns all sibling nodes that match the given tag filters.

        Args:
            tags (Set[str], optional): Required tags.
            ignore (Set[str], optional): Tags to exclude.

        Returns:
            List[Node]: The matching sibling nodes.
        """
        return list(
            filter(
                lambda element: self._tag_filter(element, tags, ignore),
                self.parent.children
            )
        )

    def __repr__(self):
        return f'<{self.label} #{self.id}' + "".join([f' {key} = {value}' for key, value in self.debug_info.items()]) + '>' 

    def debug(self, spaces: int = 4):
        """
        Prints the node hierarchy in a structured, indented format.

        Args:
            spaces (int, optional): The number of spaces per indentation level.
        """
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
        """
        Sends a message to all descendants of this node.

        Args:
            type (str): The type of the message.
            content (dict): The message content.
            _source (Node, optional): The original sender. Defaults to self.

        Returns:
            bool: False if propagation is stopped, True otherwise.
        """
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
    """  
    Create a dictionary mapping each subclass name of cls to its reference.
    """
    subclasses = set()
    for subclass in cls.__subclasses__():
        subclasses.add(subclass)
        subclasses.update(_all_subclasses(subclass))
    return subclasses


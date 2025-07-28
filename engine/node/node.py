from engine.context.context import *
from typing import *


class Node:
    """
    Nodes are tree-like objects used to organise every aspect of your game.
    """
    def __init__(self, context:Context, label:str="Node"):
        """
        Args:
            context (Context): context the node is linked to
            label (str, optional): name of the node
        Properties:
        """
        self.context = context
        self.label = label
        self.update_ = True
        self.children = []
        self.tags = set({"@" + label})
        self.parent = None
        self.order = 0
        
    def _tag_filter(self, element:"Node", tags:Set[str], ignore:Set[str]): 
        return   all(tag in element.tags for tag in tags) \
         and not any(tag in element.tags for tag in ignore)
    
    def __children_sort(self):
        self.children.sort(key = lambda child : child.order, reverse = True)
        
    @property
    def root(self):
        """  
        root of the tree where the node is located.
        """
        if self.parent != None:
            return self.parent.root 
        return self 
        
    def link(self, child:"Node"):
        """ 
        add a new child the node.
        """
        self.children.append(child)
        child.parent = self
        
    def unlink(self):
        """  
        separate the node from it's parent
        """
        if self.parent:
            self.parent.children.remove(self)
            self.parent = None

    def update(self):
        """  
        Abstract method called when the node is updated.
        """
        print(self, end=" ")
        print("updated")
    
    def update_all(self):
        """ 
        update the node and all it's children.
        """
        if self.update_:
            self.update()
            self.__children_sort()
            for child in self.children:
                child.update_all()
                
    def get_descendants(self, tags:Set[str] = set({}), ignore:Set[str] = set({})):
        """  
        get the descendants of the node in the tree hierarchy.
        Args:
            tags (Set[str], optional): tags that every searched nodes must include.
            ignore (Set[str], optional): tags that every searched nodes must not include.
        """
        output = []
        def recursive_search(self):
            self.__children_sort()
            for child in self.children:
                if self._tag_filter(child, tags, ignore):
                    output.append(child)
                recursive_search(child)
        recursive_search(self)
        return output
    
    def get_ancestors(self, tags:Set[str] = set({}), ignore:Set[str] = set({})):
        """  
        get the ancestors of the node in the tree hierarchy.
        Args:
            tags (Set[str], optional): tags that every searched nodes must include.
            ignore (Set[str], optional): tags that every searched nodes must not include.
        """
        output = []
        def recursive_search(self):
            if self._tag_filter(self, tags, ignore):
                output.append(self)
                if self.parent != None:
                    recursive_search(self.parent)
        if self.parent != None:
            recursive_search(self.parent)
        return output
    
    def get_siblings(self, tags:Set[str] = set({}), ignore:Set[str] = set({})):
        """  
        get the siblings of the node in the tree hierarchy.
        Args:
            tags (Set[str], optional): tags that every searched nodes must include.
            ignore (Set[str], optional): tags that every searched nodes must not include.
        """
        return list(
            filter(
                lambda element : self._tag_filter(element, tags, ignore), 
                self.parent.children
            )
        )
            
    def __repr__(self):
        return f'<{self.label}>'
    
    def debug(self, spaces:int = 4):
        """  
        displays the node in the console with a markdown format.
        Args:
            spaces (int, optional): lenght of each identation.
        """
        def recursive_helper(self, id):  
            if self.children == []:
                print(" "*(id * spaces) + self.__repr__()[:-1] + "/>")
            else:
                print(" "*(id * spaces) + self.__repr__())
                for child in self.children:
                    recursive_helper(child, id+1)
                print(" "*(id * spaces) + self.__repr__()[:-1] + "/>")
        recursive_helper(self, 0)
        

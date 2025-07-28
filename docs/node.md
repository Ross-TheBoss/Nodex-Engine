# `Node` Class Documentation

`Node` objects are tree-like elements used to structure and manage the logic and components of your game. Each node can have children, a parent, tags, and custom behavior via methods.

---

## Constructor

### `__init__(self, context: Context, label: str = "Node")`

Initializes a new node.

- **Parameters:**
  - `context (Context)`: The game context this node is attached to.
  - `label (str, optional)`: A human-readable name for the node. Defaults to `"Node"`.

---

## Properties

### `root: Node`
Returns the root node of the current node's hierarchy (the top-most parent).

---

## Attributes

| Name        | Type                | Description                                  |
|-------------|---------------------|----------------------------------------------|
| `context`   | `Context`           | The context object this node is part of.     |
| `label`     | `str`               | The name of the node.                        |
| `update_`   | `bool`              | Whether the node is active in updates.       |
| `children`  | `List[Node]`        | List of child nodes.                         |
| `tags`      | `Set[str]`          | Tags used to categorize the node.            |
| `parent`    | `Optional[Node]`    | The parent of the node, if any.              |
| `order`     | `int`               | Sorting priority (higher means earlier).     |

---

## Tree Management Methods

### `link(self, child: Node)`
Adds a child to this node.

- **Parameters:**
  - `child (Node)`: The node to add as a child.

---

### `unlink(self)`
Detaches this node from its parent.

---

### `__children_sort(self)`
Sorts the node’s children by descending `order`.

---

## Tree Traversal Methods

### `get_descendants(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List[Node]`

Recursively returns all descendant nodes that match given tag filters.

- **Parameters:**
  - `tags`: Required tags.
  - `ignore`: Tags to exclude.
- **Returns:** `List[Node]`

---

### `get_ancestors(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List[Node]`

Returns all ancestor nodes matching the tag filters.

- **Parameters:**
  - `tags`: Required tags.
  - `ignore`: Tags to exclude.
- **Returns:** `List[Node]`

---

### `get_siblings(self, tags: Set[str] = set(), ignore: Set[str] = set()) -> List[Node]`

Returns sibling nodes (same parent) matching the tag filters.

- **Returns:** `List[Node]`

---

## Update Methods

### `update(self)`

Called to update the node logic. Meant to be overridden in subclasses.

---

### `update_all(self)`

Recursively updates the node and all its children.

---

## Messaging System

### `message(self, type: str, content: dict = {}, _source: Node = None) -> bool`

Sends a message to all descendants of the node, depending on how each one responds.

- **Parameters:**
  - `type`: Message type.
  - `content`: Message payload.
  - `_source`: Origin node. Defaults to self.
- **Returns:** 
  - `True` to indicate full propagation.
  - `False` if interrupted by a node.

---

### `on_message(self, type: str, content: dict, source: Node) -> bool | None`

Handles incoming messages.

- **Returns:**
  - `True`: Continue to propagate to children.
  - `False`: Stop message propagation entirely.
  - `None`: Do not propagate to children of this node, but continue elsewhere.

---

## Debugging

### `__repr__(self) -> str`

Returns a string representation like `<NodeLabel>`.

---

### `debug(self, spaces: int = 4)`

Displays the full subtree of this node in the console with indentation.

- **Parameters:**
  - `spaces`: Number of spaces per indentation level.

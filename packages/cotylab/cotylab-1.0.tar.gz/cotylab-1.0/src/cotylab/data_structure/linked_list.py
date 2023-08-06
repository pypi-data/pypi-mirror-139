class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None

    def __str__(self):
        return str(self.value)
    

class DoubledNode(Node):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.prev = None


class LinkedList:
    NODE_CLASS = Node
    DELIMITER = ' -> '

    def __init__(self, data=[]):
        self.head = None
        self.tail = None
        self.current = -1
        self.set_nodes(data)

    def set_nodes(self, data):
        self.head = None
        self.tail = None
        for value in reversed(data):
            self.insert_node(value)
    
    def insert_node(self, value, base_node=None, after=True):
        node = self.NODE_CLASS(value)
        if base_node is None:
            if self.tail is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                self.tail = node
        elif after:
            node.next = base_node.next
            base_node.next = node
        else:
            current_node = self.head
            prev_node = None
            while current_node is not None:
                if current_node == base_node:
                    break
                prev_node = current_node
                current_node = current_node.next
            if prev_node is None:
                node.next = self.head
                self.head = node
            else:
                node.next = base_node
                prev_node.next = node
    
    def delete_node(self, node):
        current_node = self.head
        prev_node = None
        while current_node is not None:
            if current_node == node:
                if prev_node is None:
                    self.head = current_node.next
                else:
                    prev_node.next = current_node.next
                del current_node
                return True
            prev_node = current_node
            current_node = current_node.next
        return False

    def next(self):
        if self.current == -1:
            self.current = self.head
        elif self.current is not None:
            self.current = self.current.next
        else:
            return None
        return self.current

    def set_current(self, node):
        self.current = node

    def go_to_head(self):
        self.set_current(self.head)

    def go_to_tail(self):
        self.set_current(self.tail)

    def __str__(self):
        values = []
        current_node = self.head
        while current_node is not None:
            values.append(str(current_node.value))
            current_node = current_node.next
        return self.DELIMITER.join(values)


class DoubledLinkedList(LinkedList):
    NODE_CLASS = DoubledNode
    DELIMITER = ' <-> '

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def insert_node(self, value, base_node=None, after=True):
        node = self.NODE_CLASS(value)
        if base_node is None:
            if self.tail is None:
                self.head = node
                self.tail = node
            else:
                self.tail.next = node
                node.prev = self.tail
                self.tail = node
        elif after:
            node.next = base_node.next
            node.prev = base_node
            base_node.next = node
            if node.next is None:
                self.tail = node
        else:
            if base_node.prev is None:
                node.next = self.head
                self.head = node
            else:
                node.next = base_node
                node.prev = base_node.prev
                base_node.prev = node

    def prev(self):
        if self.current == -1:
            self.current = self.tail
        elif self.current is not None:
            self.current = self.current.prev
        else:
            return None
        return self.current


class CircularLinkedList(LinkedList):
    def next(self):
        current = super().next()
        if current is None:
            self.current = self.head
        return self.current

class Stack:
    def __init__(self):
        self.elements = []

    def push(self, element):
        self.elements.append(element)

    def pop(self):
        if not self.empty():
            return self.elements.pop()
        return None

    def top(self):
        if not self.empty():
            return self.elements[-1]
        return None

    def empty(self):
        return not self.elements

    def clear(self):
        self.elements = []

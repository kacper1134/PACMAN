import pygame as pg
from settings import *
from structures.stack import Stack


class Node:
    def __init__(self, row, col):
        self.row, self.column = row, col
        self.position = Vector2Dim(col * TILE_WIDTH, row * TILE_HEIGHT)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}
        self.portal_node = None
        self.portal_val = 0

    def draw(self, screen):
        for neighbor in self.neighbors.keys():
            if self.neighbors[neighbor]:
                start = self.position.to_tuple()
                end = self.neighbors[neighbor].position.to_tuple()
                pg.draw.line(screen, WHITE, start, end, 4)
                pg.draw.circle(screen, RED, self.position.to_int(), 12)


class NodeGroup:
    def __init__(self, tile_map_file):
        self.nodes = []
        self.tile_map_file = tile_map_file
        self.grid = None
        self.stack_of_nodes = Stack()
        self.portal_symbols = ["1"]
        self.node_symbols = [NODE_SYMBOL] + self.portal_symbols
        self.create_node_list()
        self.setup_portal_nodes()

    def create_node_list(self):
        self.grid = self.read_tile_map()
        start_node = self.find_first_node(len(self.grid), len(self.grid[0]))
        self.stack_of_nodes.push(start_node)

        while not self.stack_of_nodes.empty():
            current_node = self.stack_of_nodes.pop()
            self.add_node(current_node)

            left_neighbor = self.get_neighbor_node(LEFT, current_node.row, current_node.column - 1)
            right_neighbor = self.get_neighbor_node(RIGHT, current_node.row, current_node.column + 1)
            up_neighbor = self.get_neighbor_node(UP, current_node.row - 1, current_node.column)
            down_neighbor = self.get_neighbor_node(DOWN, current_node.row + 1, current_node.column)

            current_node_neighbors = [up_neighbor, down_neighbor, left_neighbor, right_neighbor]

            current_node.neighbors = {key: current_node_neighbors[index] for index, key in
                                      enumerate(current_node.neighbors.keys())}

            for neighbor in current_node_neighbors:
                self.add_node_to_stack(neighbor)

    def read_tile_map(self):
        with open(self.tile_map_file, "r") as f:
            return [row.strip().split(" ") for row in f]

    def find_first_node(self, number_of_rows, number_of_cols):
        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if self.grid[row][col] in self.node_symbols:
                    node = Node(row, col)

                    if self.grid[row][col] in self.portal_symbols:
                        node.portal_val = self.grid[row][col]

                    return node
        return None

    def get_node(self, x, y):
        for node in self.nodes:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    def get_neighbor_node(self, direction, row, column):
        aux = self.follow_path(direction, row, column)
        return self.get_node_from_nodes(aux)

    def get_node_from_nodes(self, node):
        if node:
            for current_node in self.nodes:
                if node.row == current_node.row and node.column == current_node.column:
                    return current_node
        return node

    def add_node(self, node):
        is_node_in_nodes = self.node_in_nodes(node)
        if not is_node_in_nodes:
            self.nodes.append(node)

    def add_node_to_stack(self, neighbor_node):
        if neighbor_node and not self.node_in_nodes(neighbor_node):
            self.stack_of_nodes.push(neighbor_node)

    def node_in_nodes(self, node):  # check if node is already in the list
        for current_node in self.nodes:
            if node.position.x == current_node.position.x and node.position.y == current_node.position.y:
                return True
        return False

    def follow_path(self, direction, row, col):
        number_of_rows = len(self.grid)
        number_of_cols = len(self.grid[0])

        if direction == LEFT and col >= 0:
            return self.path_to_follow(LEFT, row, col, HORIZONTAL_PATH_SYMBOL)
        elif direction == RIGHT and col < number_of_cols:
            return self.path_to_follow(RIGHT, row, col, HORIZONTAL_PATH_SYMBOL)
        elif direction == UP and row >= 0:
            return self.path_to_follow(UP, row, col, VERTICAL_PATH_SYMBOL)
        elif direction == DOWN and row < number_of_rows:
            return self.path_to_follow(DOWN, row, col, VERTICAL_PATH_SYMBOL)
        else:
            return None

    def path_to_follow(self, direction, row, col, path_symbol):
        symbols = [path_symbol] + self.node_symbols

        if self.grid[row][col] in symbols:
            while self.grid[row][col] not in self.node_symbols:
                row = row + 1 if direction == DOWN else row - 1 if direction == UP else row
                col = col + 1 if direction == RIGHT else col - 1 if direction == LEFT else col
            node = Node(row, col)

            if self.grid[row][col] in self.portal_symbols:
                node.portal_val = self.grid[row][col]
            return node

        return None

    def setup_portal_nodes(self):
        portal = {}

        for i in range(len(self.nodes)):
            if self.nodes[i].portal_val != 0:
                if self.nodes[i].portal_val not in portal.keys():
                    portal[self.nodes[i].portal_val] = [i]
                else:
                    portal[self.nodes[i].portal_val] += [i]

        for key in portal.keys():
            first_node, second_node = portal[key]
            self.nodes[first_node].portal_node = self.nodes[second_node]
            self.nodes[second_node].portal_node = self.nodes[first_node]

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

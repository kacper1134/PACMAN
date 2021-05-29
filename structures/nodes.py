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

        self.ghost_house_guide = False
        self.ghost_house_entrance = False
        self.ghost_spawn = False

        self.pacman_start_position = False
        self.blinky_start_position = False
        self.inky_start_position = False
        self.pinky_start_position = False
        self.clyde_start_position = False

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
        self.ghost_home_nodes = []
        self.tile_map_file = tile_map_file

        self.grid = self.read_tile_map()
        self.ghost_house_grid = GHOST_HOUSE

        self.stack_of_nodes = Stack()
        self.portal_symbols = ["1"]
        self.node_symbols = [NODE_SYMBOL, HOUSE_SYMBOL, GHOST_SPAWN_SYMBOL, PACMAN_START_NODE,
                             BLINKY_START_NODE, INKY_START_NODE, CLYDE_START_NODE] + self.portal_symbols

        self.create_node_list(self.grid, self.nodes)
        self.create_node_list(self.ghost_house_grid, self.ghost_home_nodes)

        self.setup_portal_nodes()
        self.setup_house_nodes()

    def create_node_list(self, grid, node_list):
        start_node = self.find_first_node(grid)
        self.stack_of_nodes.push(start_node)

        while not self.stack_of_nodes.empty():
            current_node = self.stack_of_nodes.pop()

            self.add_node(current_node, node_list)

            left_neighbor = self.get_neighbor_node(grid, node_list, LEFT, current_node.row, current_node.column - 1)
            right_neighbor = self.get_neighbor_node(grid, node_list, RIGHT, current_node.row, current_node.column + 1)
            up_neighbor = self.get_neighbor_node(grid, node_list, UP, current_node.row - 1, current_node.column)
            down_neighbor = self.get_neighbor_node(grid, node_list, DOWN, current_node.row + 1, current_node.column)

            current_node_neighbors = [up_neighbor, down_neighbor, left_neighbor, right_neighbor]

            current_node.neighbors = {key: current_node_neighbors[index] for index, key in
                                      enumerate(current_node.neighbors.keys())}

            for neighbor in current_node_neighbors:
                self.add_node_to_stack(neighbor, node_list)

        return node_list

    def read_tile_map(self):
        with open(self.tile_map_file, "r") as f:
            return [row.strip().split(" ") for row in f]

    def find_first_node(self, grid):
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])

        for row in range(number_of_rows):
            for col in range(number_of_cols):
                if grid[row][col] in self.node_symbols:
                    node = Node(row, col)

                    if grid[row][col] in self.portal_symbols:
                        node.portal_val = grid[row][col]

                    if grid[row][col] == BLINKY_START_NODE:
                        node.blinky_start_position = True

                    return node
        return None

    def get_node(self, x, y):
        for node in self.nodes:
            if node.position.x == x and node.position.y == y:
                return node
        return None

    def get_neighbor_node(self, grid, nodes, direction, row, column):
        aux = self.follow_path(grid, direction, row, column)
        return self.get_node_from_nodes(aux, nodes)

    def get_node_from_nodes(self, node, nodes):
        if node:
            for current_node in nodes:
                if node.row == current_node.row and node.column == current_node.column:
                    return current_node
        return node

    def add_node(self, node, nodes_list):
        is_node_in_nodes = self.node_in_nodes(node, nodes_list)
        if not is_node_in_nodes:
            nodes_list.append(node)

    def add_node_to_stack(self, neighbor_node, nodes_list):
        if neighbor_node and not self.node_in_nodes(neighbor_node, nodes_list):
            self.stack_of_nodes.push(neighbor_node)

    def node_in_nodes(self, node, nodes):  # check if node is already in the list
        for current_node in nodes:
            if node.position.x == current_node.position.x and node.position.y == current_node.position.y:
                return True
        return False

    def follow_path(self, grid, direction, row, col):
        number_of_rows = len(grid)
        number_of_cols = len(grid[0])

        if direction == LEFT and col >= 0:
            return self.path_to_follow(grid, LEFT, row, col, HORIZONTAL_PATH_SYMBOL)
        elif direction == RIGHT and col < number_of_cols:
            return self.path_to_follow(grid, RIGHT, row, col, HORIZONTAL_PATH_SYMBOL)
        elif direction == UP and row >= 0:
            return self.path_to_follow(grid, UP, row, col, VERTICAL_PATH_SYMBOL)
        elif direction == DOWN and row < number_of_rows:
            return self.path_to_follow(grid, DOWN, row, col, VERTICAL_PATH_SYMBOL)
        else:
            return None

    def path_to_follow(self, grid, direction, row, col, path_symbol):
        symbols = [path_symbol] + self.node_symbols

        if grid[row][col] in symbols:
            while grid[row][col] not in self.node_symbols:
                row = row + 1 if direction == DOWN else row - 1 if direction == UP else row
                col = col + 1 if direction == RIGHT else col - 1 if direction == LEFT else col
            node = Node(row, col)

            if grid[row][col] == HOUSE_SYMBOL:
                node.ghost_house_guide = True

            if grid[row][col] == GHOST_SPAWN_SYMBOL:
                node.ghost_spawn = True
                node.pinky_start_position = True

            if grid[row][col] == INKY_START_NODE:
                node.inky_start_position = True

            if grid[row][col] == CLYDE_START_NODE:
                node.clyde_start_position = True

            if grid[row][col] == PACMAN_START_NODE:
                node.pacman_start_position = True

            if grid[row][col] in self.portal_symbols:
                node.portal_val = grid[row][col]
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

    def setup_house_nodes(self):
        house_entrance_node = Node(0, 0)
        for node in self.nodes:
            if node.ghost_house_guide:
                house_entrance_node = node
        house_entrance_position = (house_entrance_node.position + house_entrance_node.neighbors[LEFT].position) / 2
        house_entrance_vector = Vector2Dim(house_entrance_position.x, house_entrance_position.y)
        house_start_vector = Vector2Dim(self.ghost_home_nodes[0].position.x, self.ghost_home_nodes[0].position.y)

        for node in self.ghost_home_nodes:
            node.position -= house_start_vector
            node.position += house_entrance_vector
            self.add_node(node, self.nodes)

        right_neighbor = self.get_node_from_nodes(house_entrance_node, self.nodes)
        left_neighbor = self.get_node_from_nodes(house_entrance_node.neighbors[LEFT], self.nodes)
        house_node = self.get_node_from_nodes(self.ghost_home_nodes[0], self.nodes)

        right_neighbor.neighbors[LEFT] = house_node
        left_neighbor.neighbors[RIGHT] = house_node
        house_node.neighbors[RIGHT] = right_neighbor
        house_node.neighbors[LEFT] = left_neighbor

        self.ghost_home_nodes[0].ghost_house_entrance = True

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)
        for node in self.ghost_home_nodes:
            node.draw(screen)

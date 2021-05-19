import pygame as pg
from structures.vector import Vector2Dim
from settings import *


class Node:
    def __init__(self, row, col):
        self.row, self.column = row, col
        self.position = Vector2Dim(col * TILE_WIDTH, row * TILE_HEIGHT)
        self.neighbors = {UP: None, DOWN: None, LEFT: None, RIGHT: None}

    def draw(self, screen):
        for neighbor in self.neighbors.keys():
            if self.neighbors[neighbor]:
                start = self.position.to_tuple()
                end = self.neighbors[neighbor].position.to_tuple()
                pg.draw.line(screen, WHITE, start, end, 4)
                pg.draw.circle(screen, RED, self.position.to_int(), 12)


class NodeGroup:
    def __init__(self):
        self.nodes = []

    def setupTestNodes(self):
        nodeA = Node(5, 5)
        nodeB = Node(5, 10)
        nodeC = Node(10, 5)
        nodeD = Node(10, 10)
        nodeE = Node(10, 13)
        nodeF = Node(20, 5)
        nodeG = Node(20, 13)
        nodeA.neighbors[RIGHT] = nodeB
        nodeA.neighbors[DOWN] = nodeC
        nodeB.neighbors[LEFT] = nodeA
        nodeB.neighbors[DOWN] = nodeD
        nodeC.neighbors[UP] = nodeA
        nodeC.neighbors[RIGHT] = nodeD
        nodeC.neighbors[DOWN] = nodeF
        nodeD.neighbors[UP] = nodeB
        nodeD.neighbors[LEFT] = nodeC
        nodeD.neighbors[RIGHT] = nodeE
        nodeE.neighbors[LEFT] = nodeD
        nodeE.neighbors[DOWN] = nodeG
        nodeF.neighbors[UP] = nodeC
        nodeF.neighbors[RIGHT] = nodeG
        nodeG.neighbors[UP] = nodeE
        nodeG.neighbors[LEFT] = nodeF
        self.nodes = [nodeA, nodeB, nodeC, nodeD, nodeE, nodeF, nodeG]

    def draw(self, screen):
        for node in self.nodes:
            node.draw(screen)

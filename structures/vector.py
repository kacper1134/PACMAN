import math


class Vector2Dim:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.margin = 0.000001

    def magnitude_squared(self):
        return self.x ** 2 + self.y ** 2

    def magnitude(self):
        return math.sqrt(self.magnitude_squared())

    def normalize(self):
        magnitude = self.magnitude()
        if magnitude != 0:
            return self.__div__(magnitude)
        return None

    def dot(self, other):
        return self.x * other.x, self.y * other.y

    def copy(self):
        return Vector2Dim(self.x, self.y)

    def to_tuple(self):
        return self.x, self.y

    def to_int(self):
        return int(self.x), int(self.y)

    def __add__(self, other):
        return Vector2Dim(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2Dim(self.x - other.x, self.y - other.y)

    def __neg__(self):
        return Vector2Dim(-self.x, -self.y)

    def __mul__(self, scalar):
        return Vector2Dim(self.x * scalar, self.y * scalar)

    def __div__(self, scalar):
        if scalar != 0:
            return Vector2Dim(self.x / scalar, self.y / scalar)
        else:
            return None

    def __truediv__(self, scalar):
        return self.__div__(scalar)

    def __eq__(self, other):
        return abs(self.x - other.x) < self.margin and abs(self.y - other.y) < self.margin

    def __hash__(self):
        return id(self)

    def __str__(self):
        return "< " + str(self.x) + ", " + str(self.y) + " >"

from __future__ import annotations
from .paper_types import types

Number = int | float
"""type alias"""
Vector2 = tuple[Number, Number]
"""type alias (Number,Number)"""
Vector3 = tuple[Number, Number, Number]
"""type alias (Number,Number,Number)"""
Vector = Vector2 | Vector3
"""type alias"""


def vector2str(vector: Vector):
    if len(vector) == 3 and vector[2] is not None:
        x, y, z = vector
        return f"[{x} {y} {z}]"
    else:
        x, y = vector[:2]
        return f"[{x} {y}]"


class Command:
    pass


class StringCommand(Command):

    def __init__(self, string: str):
        self.string = string

    def __str__(self):
        return self.string


class Comment(Command):

    def __init__(self, message: str):
        self.message = message

    def __str__(self):
        return f"{{{self.message}}}"


class Paper(Command):

    def __init__(self, *args: str | tuple[Vector2, Vector2, Vector2, Vector2], new=True):
        if len(args) == 1:
            arg: str = args[0]
            if arg not in types:
                raise ValueError(f"paper type must be one of {types}")
            self.args = arg
        elif len(args) == 4:
            args: tuple[Vector2, Vector2, Vector2, Vector2] = args
            self.args = " ".join(vector2str(a) for a in args)
        else:
            raise ValueError("Paper argument are either type (1 string) or corners (4 [number,number] tuples)")
        self.new = None if new is None else New()

    def __str__(self):
        ret = f"paper {self.args}"
        if (self.new):
            ret += f" {self.new}"
        return ret


class Corner(Command):

    def __init__(self, x: Number, y: Number):
        self.coords = (x, y)

    def __str__(self):
        p = vector2str(self.coords)
        return f"corner {p}"


class Plane(Command):

    def __init__(self, point: Vector, normal: Vector3):
        self.point = point
        self.normal = normal

    def __str__(self):
        p = vector2str(self.point)
        n = vector2str(self.normal)
        return f"plane {p} {n}"


class PlanePoint(Command):

    def __init__(self, x: Number, y: Number, z: Number = None):
        self.coords = (x, y, z)

    def __str__(self):
        p = vector2str(self.coords)
        return f"planepoint {p}"


class PlaneNormal(Command):

    def __init__(self, x: Number, y: Number, z: Number):
        self.coords = (x, y, z)

    def __str__(self):
        n = vector2str(self.coords)
        return f"planenormal {n}"


class PlaneThrough(Command):

    def __init__(self, p1: Vector, p2: Vector, p3: Vector):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        p1 = vector2str(self.p1)
        p2 = vector2str(self.p2)
        p3 = vector2str(self.p3)
        return f"planethrough {p1} {p2} {p3}"


class AngleBisector(Command):

    def __init__(self, p1: Vector, p2: Vector, p3: Vector):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3

    def __str__(self):
        p1 = vector2str(self.p1)
        p2 = vector2str(self.p2)
        p3 = vector2str(self.p3)
        return f"angle-bisector {p1} {p2} {p3}"


class Target(Command):

    def __init__(self, x: Number, y: Number):
        self.coords = (x, y)

    def __str__(self):
        p = vector2str(self.coords)
        return f"target {p}"


class Angle(Command):

    def __init__(self, value: Number):
        self.value = value

    def __str__(self):
        return f"angle {self.value}"


class New(Command):

    def __str__(self):
        return "new"


class Reflect(Command):

    def __str__(self):
        return "reflect"


class Rotate(Command):

    def __str__(self):
        return "rotate"


class Cut(Command):

    def __str__(self):
        return "cut"

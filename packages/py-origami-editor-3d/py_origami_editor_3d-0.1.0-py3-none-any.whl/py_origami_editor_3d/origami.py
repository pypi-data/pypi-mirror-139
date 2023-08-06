import os
from .commands import *


class Origami:

    def __init__(self):
        pass
        self.commands = [
            StringCommand("version 1"),
        ]

    def command(self, command: Command):
        self.commands.append(command)
        return self

    def comment(self, *args, **kw):
        return self.command(Comment(*args, **kw))

    def paper(self, *args, **kw):
        return self.command(Paper(*args, **kw))

    def corner(self, *args, **kw):
        return self.command(Corner(*args, **kw))

    def plane(self, *args, **kw):
        return self.command(Plane(*args, **kw))

    def planePoint(self, *args, **kw):
        return self.command(PlanePoint(*args, **kw))

    def planeNormal(self, *args, **kw):
        return self.command(PlaneNormal(*args, **kw))

    def planeThrough(self, *args, **kw):
        return self.command(PlaneThrough(*args, **kw))

    def angleBisector(self, *args, **kw):
        return self.command(AngleBisector(*args, **kw))

    def target(self, *args, **kw):
        return self.command(Target(*args, **kw))

    def angle(self, *args, **kw):
        return self.command(Angle(*args, **kw))

    def new(self, *args, **kw):
        return self.command(New(*args, **kw))

    def reflect(self, *args, **kw):
        return self.command(Reflect(*args, **kw))

    def rotate(self, *args, **kw):
        return self.command(Rotate(*args, **kw))

    def cut(self, *args, **kw):
        return self.command(Cut(*args, **kw))

    def save(self, fileName: str):
        _, ext = os.path.splitext(fileName)
        if not ext:
            fileName += ".txt"
        #
        with open(fileName, "w") as f:
            f.writelines(f"{line}\n" for line in self.commands)

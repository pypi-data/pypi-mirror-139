from .constans import *
from .Base import Svg_Base, Shape_Base, Text_Base, Gradient_Base

class Svg(Svg_Base):
    def __init__(self, width, height, viewBox, x=0, y=0, style={}):
        self.tag_specs = {
            "width": width,
            "height": height,
            "viewBox": viewBox,
            # "x": x,
            # "y": y,
        }
        super().__init__("svg", self.tag_specs, style, end_tag=True)


class Rect(Shape_Base):
    def __init__(self, parent, width, height, x=0, y=0, rx=0, ry=0, style={}):
        self.tag_specs = {
            "width": width,
            "height": height,
            "x": x,
            "y": y,
            "rx": rx,
            "ry": ry,
        }
        super().__init__(parent, "rect", self.tag_specs, style)

class Circle(Shape_Base):
    def __init__(self, parent, cx, cy, r, style={}):
        self.tag_specs = {
            "cx": cx,
            "cy": cy,
            "r": r,
        }
        super().__init__(parent, "circle", self.tag_specs, style)


class Ellipse(Shape_Base):
    def __init__(self, parent, cx, cy, rx, ry, style={}):
        self.tag_specs = {
            "cx": cx,
            "cy": cy,
            "rx": rx,
            "ry": ry,
        }
        super().__init__(parent, "ellipse", self.tag_specs, style)


class Line(Shape_Base):
    def __init__(self, parent, x1, x2, y1, y2, style={}):
        self.tag_specs = {
            "x1": x1,
            "x2": x2,
            "y1": y1,
            "y2": y2,
        }
        super().__init__(parent, "line", self.tag_specs, style)


class Polygon(Shape_Base):
    def __init__(self, parent, points, style={}):
        if(type(points) != str):
            points =self.convert_points(points)
        self.tag_specs = {
            "points": points,
        }
        super().__init__(parent, "polygon", self.tag_specs, style)

class Polyline(Shape_Base):
    def __init__(self, parent, points, style={}):
        if(type(points) != str):
            points =self.convert_points(points)
        self.tag_specs = {
            "points": points,
        }
        super().__init__(parent, "polyline", self.tag_specs, style)

class Text(Text_Base):
    def __init__(self, parent, text, x, y, style={}):
        self.tag_specs = {
            "x": x,
            "y": y,
        }
        super().__init__(parent, self.tag_specs, style, inline=text)

class Path(Shape_Base):
    def __init__(self, parent, d, style={}):
        self.tag_specs = {
            "d": d
        }
        super().__init__(parent, "path", self.tag_specs, style)


class Defs(Svg_Base):
    def __init__(self, parent):
        self.parent = parent
        self.parent.inline.append(self)
        super().__init__("defs", {}, {}, end_tag=True, inline=[])

class RadialGradient(Gradient_Base):
    def __init__(self, parent, id, cx="50%", cy="50%", r="50%", fx="0%", fy="0%", style={}):
        self.tag_specs = {
            "id": id,
            "cx": cx,
            "cy": cy,
            "r": r,
            "fx": fx,
            "fy": fy,
        }
        super().__init__(parent, id, "radialGradient", self.tag_specs, style)

class LinearGradient(Gradient_Base):
    def __init__(self, parent, id, x1="0%", y1="0%", x2="100%", y2="100%", style={}):
        self.tag_specs = {
            "id": id,
            "x1": x1,
            "y1": y1,
            "x2": x2,
            "y2": y2,
        }
        super().__init__(parent, id, "linearGradient", self.tag_specs, style)

class Stop(Shape_Base):
    def __init__(self, parent, offset, color, opacity, style={}):
        self.tag_specs = {
            "offset": offset,
            "stop-color": color,
            "stop-opacity": opacity,
        }
        super().__init__(parent, "stop", self.tag_specs, style)
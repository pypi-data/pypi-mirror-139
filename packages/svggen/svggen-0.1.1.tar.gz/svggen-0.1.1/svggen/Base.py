from constans import *


class Svg_Base():
    # It have inline but it have not parent
    def __init__(self, tag_name, tag_specs, style={}, end_tag=False, inline=[]):
        self.tag_name = tag_name
        self.tag_specs = tag_specs
        self.style = style
        self.end_tag = end_tag
        if(end_tag):
            self.inline = inline

        
    def create_tag(self):
        specs = ""
        for name, value in self.tag_specs.items():
            spec = "{} = {} ".format(name, f"'{value}'")
            specs += spec
        if(type(self.style) != str):
            if self.style:
                style = STYLE + EQUAL + self.create_style()
            else:
                style = ""
        else:
            style = STYLE + EQUAL + f"'{self.style}'"
        tag = STARTER + self.tag_name + SPACE + specs + SPACE + style
        
        if(self.end_tag):
            tag += END
            tag += self.create_inline()
            tag += STARTER + CLOSER + self.tag_name + END
        else:
            tag += CLOSER + END
        return tag

    def create_style(self):
        style = ""
        # print(f"{self.tag_name}: {type(self.style)}")
        for name, value in self.style.items():
            style += "{}{}{}{}".format(name, COLON, f"{value}", SEMICOLON)
        if style:
            return f"'{style}'"
        else:
            return "''"

    def create_inline(self):
        if(type(self.inline) != str):
            inline = ""
            for shape in self.inline:
                inline += shape.create_tag()
            return inline
        else:
            return self.inline


class Shape_Base(Svg_Base):
    #It have parent. But it have not inline
    def __init__(self, parent, tag_name, tag_specs, style={}, end_tag=False):
        super().__init__(tag_name, tag_specs, style, end_tag)
        self.parent = parent
        self.parent.inline.append(self)

    def convert_points(self, points):
        # Point example [(0,100), (40, 50), (70, 80), (60, 20)]
        res = ""
        for x, y in points:
            res += f"{x},{y} "
        return res
        

class Text_Base(Svg_Base):
    #It have inline and parent. But its inline is only text.
    def __init__(self, parent, tag_specs, style={}, inline=""):
        super().__init__("text", tag_specs, style, end_tag=True, inline=inline)
        self.parent = parent
        self.parent.inline.append(self)

class Gradient_Base(Svg_Base):
    #It have parent and inline.
    def __init__(self, parent, id, tag_name, tag_specs, style={}):
        super().__init__(tag_name, tag_specs, style, end_tag=True, inline=[])
        self.parent = parent
        self.parent.inline.append(self)
        self.id = id

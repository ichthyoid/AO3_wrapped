from PIL import Image, ImageDraw, ImageFont
import io
import math

class Textbox:
    def __init__(self, text, x, y, w, h, font, color=(0,0,0),align="center",preserve_breaks=False,outline=False,spacing=4,max_size=10000):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.font = font
        self.color = color
        self.align = align
        self.preserve_breaks = preserve_breaks
        self.outline = outline
        self.spacing = spacing
        self.max_size=max_size
    def draw(self, image):
        # set position to middle if centering requested
        if self.x == "c":
            x = image.wm
        else:
            x = self.x
        if self.y == "c":
            y = image.hm
        else:
            y = self.y
        # get line breaks and font size to fit in bounding box
        lines, font = self.getlines(image.draw, 1)
        # draw bounding box
        if self.outline:
            image.draw.rectangle([(x-self.w/2, y-self.h/2),(x+self.w/2, y+self.h/2)], width=10, outline=(0,0,0))
        # draw text
        image.draw.multiline_text((x, y), lines, fill=self.color, font=font, anchor="mm", spacing=self.spacing, align=self.align)
    def getlines(self, image, font_size):
        # create font at current size
        font = ImageFont.truetype(self.font, font_size)
        # greedy line break algorithm
        if not self.preserve_breaks:
            words = self.text.split()
            #print(words)
            line_list = [words.pop(0)]
            for word in words:
                #print(word)
                line = line_list[-1] + " " + word
                length = image.textlength(line, font=font)
                #print(length)
                if length < self.w:
                    line_list[-1] = line
                else:
                    line_list.append(word)
            lines = "\n".join(line_list)
        else:
            lines = self.text
        # test if current font size is too large for bounding box
        left, top, right, bottom = image.multiline_textbbox((0,0),lines, font=font)
        # if outsize bounding box or font size constraints, ask for previous font size
        if bottom > self.h or right > self.w or font_size > self.max_size:
            return None
        else:
            # if within bounding box and font size constraints, try larger font
            # listen, this is a terrible way to do this but oh well
            res = self.getlines(image, font_size+1)
            if res is not None:
                # if larger font succeeds, return larger
                return res
            else:
                #if larger font fails, return current
                return lines, font

class Page:
    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.w, self.h = self.image.size
        self.draw = ImageDraw.Draw(self.image)
        self.wm = self.w/2
        self.hm = self.h/2
    def save(self, name, file_format='PNG'):
        self.image.save(name, format=file_format)
    def display(self):
        buf = io.BytesIO()
        self.image.save(buf, format='PNG')
        return buf.getvalue()

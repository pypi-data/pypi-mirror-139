import os
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


FONTS_DIR = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'fonts')
DEFAULT_FONT = os.path.join(FONTS_DIR, 'Monaco.ttf')


class FinishedCaptcha():
    def __init__(self, image, answer):
        self.image = image
        self.answer = answer


class Captcha:
    def __init__(self,
                width: int = 300,
                height: int = 100,
                char_number: int = 4,
                char_color: str = '#3ee6f9',
                char_type: int = 1,
                bg_color: str = '#343232',
                gradient: str = '',
                misleading_lines: int = 0,
                misleading_dots: int = 0,
                misleading_color: str = '#e6cd79'):
        self.width = width
        self.height = height
        self.char_number = char_number
        self.char_color = char_color
        self.char_type = char_type
        self.bg_color = bg_color
        self.gradient = gradient
        self.misleading_lines = misleading_lines
        self.misleading_dots = misleading_dots
        self.misleading_color = misleading_color

        self.image = 0
        self.answer = 0

    def generate_gradient(
        self, colour1: str, colour2: str, width: int, height: int) -> Image:
        """Generate a vertical gradient."""
        base = Image.new('RGB', (width, height), colour1)
        top = Image.new('RGB', (width, height), colour2)
        mask = Image.new('L', (width, height))
        mask_data = []
        for y in range(height):
            mask_data.extend([int(255 * (y / height))] * width)
        mask.putdata(mask_data)
        base.paste(top, (0, 0), mask)
        return base


    def generate_position(self, i, font_size):
        offset_x = int(self.width / self.char_number * 0.4)
        offset_y = font_size

        space_for_char = self.width / self.char_number

        x_min = space_for_char * i + offset_x
        x_max = space_for_char * (i + 1) - offset_x

        y_min = 0
        y_max = self.height - offset_y * 1.2

        x = random.randint(int(x_min), int(x_max))
        y = random.randint(int(y_min), int(y_max))

        return x, y




    def Generate(self):
        if self.gradient:
            image = self.generate_gradient(
                self.gradient, self.bg_color, self.width, self.height)
        else:
            image = Image.new('RGB', (self.width, self.height), self.bg_color)

        if self.char_type == 1:
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
        elif self.char_type == 2:
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXY'
        elif self.char_type == 3:
            chars = 'abcdefghijklmnopqrstuvwxyz'
        elif self.char_type == 4:
            chars = '0123456789'

        answer = ''
        for i in range(self.char_number):
            char = random.choice(chars)

            answer += char

            font_size = random.randint(self.height * 0.3, self.height * 0.4)

            x, y = Captcha.generate_position(self, i, font_size)


            font = ImageFont.truetype('arial', font_size)
            #draw char
            draw = ImageDraw.Draw(image)
            draw.text((x, y), char, self.char_color, font)

        if self.misleading_lines > 0:
            for _ in range(self.misleading_lines):
                x1 = random.randint(0, self.width)
                y1 = random.randint(0, self.height)
                x2 = random.randint(0, self.width)
                y2 = random.randint(0, self.height)
                draw.line((x1, y1, x2, y2), fill=self.misleading_color, width=4)

        if self.misleading_dots > 0:
            for _ in range(self.misleading_dots):
                x = random.randint(0, self.width)
                y = random.randint(0, self.height)
                radius = random.randint(0, self.width / 30)
                draw.ellipse((x, y, x+radius, y+radius), fill=self.misleading_color)

        return FinishedCaptcha(image, answer)







from io import TextIOWrapper
from typing import List
from colors import Color, invalid_color
from PIL import Image as PILImage
import numpy as np
from parser import image_args

class Image():
    matrix: List[List[Color]]
    W: int
    H: int
    def __init__(self, W: int, H: int) -> None:
        self.W = W
        self.H = H
        self.matrix = [[None for _ in range(W)] for _ in range(H)]
    def set_value(self, row: int, column: int, color: Color):
        assert 0 <= row and row < self.H
        assert 0 <= column and column < self.W
        self.matrix[row][column] = color
    def paint(self):
        output = ''
        skips = 0
        for row in range(self.H):
            last_color = invalid_color
            for column in range(self.W):
                cur_color = self.matrix[row][column]
                if cur_color == last_color:
                    output += ' '
                    skips += 1
                else:
                    output += cur_color.bash_str()
                last_color = cur_color
            output += '\x1b[0m\n'
        print(output, end='')

def ppm_to_image(filestream: TextIOWrapper):
    first_line = filestream.readline()
    assert first_line.startswith('P3')

    data = filestream.read().split()
    W = int(data[0])
    H = int(data[1])
    colors = int(data[2])
    assert colors == 255
    image = Image(W, H)

    data = data[3:]
    iter = 0
    for row in range(H):
        for column in range(W):
            red = int(data[iter])
            green = int(data[iter+1])
            blue = int(data[iter+2])
            color = Color(red, green, blue)
            image.set_value(row, column, color)
            iter += 3
    return image

def pillow_to_image(filepath: str, W: int=40, H: int=40):
    image = PILImage.open(filepath, "r").convert('RGB').resize((W, H))
    pixel_values = list(image.getdata())

    myImage = Image(W, H)
    iter = 0
    for row in range(H):
        for column in range(W):
            color = pixel_values[iter]
            iter += 1
            myImage.set_value(row, column, Color(color[0], color[1], color[2]))
    return myImage

def create_image(filepath: str, W=None, H=None):
    if filepath.endswith('.ppm'):
        with open(filepath, 'r') as filestream:
            return ppm_to_image(filestream)
    elif filepath.endswith('.png') or filepath.endswith('.jpg'):
        return pillow_to_image(filepath, W=W, H=H)
    assert not 'Unknown file format'


if __name__ == '__main__':
    parser = image_args()
    options = parser.parse_args()
    image = create_image(options.file, H=options.H, W=options.W)
    image.paint()

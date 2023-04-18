from typing import List
from image import create_image, Image, Color
from PIL import Image as PILImage
import os
import time
import argparse

class Slides():
    W: int
    H: int
    slides: List[Image]
    def __init__(self, W: int, H: int, slides: List[Image]) -> None:
        self.W = W
        self.H = H
        self.slides = slides
    def __iter__(self):
        return iter(self.slides)
    def __next__(self):
        return next(self.slides)

def dir_to_slides(dirname: str, W: int, H: int) -> Slides:
    files = [
        os.path.join(dirname, filename) for filename in
        os.listdir(dirname)
    ]
    files = sorted(files)
    # print(files)
    images = [
        create_image(file, W, H)
        for file in files
    ]
    W = images[0].W
    H = images[0].H
    assert all([(image.H == H) and (image.W == W) for image in images])
    return Slides(W, H, images)

def reset_cursor(H: int):
    string = f'\033[{H}A'
    print(string, end='')

def cursor_down(lines: int):
    string = f'\033[{lines}B'
    print(string, end='')

def slideshow(slides: Slides, iterations: int=5, refresh: float=0.1) -> None:
    H = slides.H
    for i in range(iterations):
        for image in slides:
            image.paint()
            time.sleep(refresh)
            reset_cursor(H)
    cursor_down(H)

def gif_to_slides(filename: str, W: int, H: int):
    pilImage = PILImage.open(filename)
    images = []
    for i in range(pilImage.n_frames):
        pilImage.seek(i)
        pixel_values = list(pilImage.convert('RGB').resize((W, H)).getdata())
        myImage = Image(W, H)
        iter = 0
        for row in range(H):
            for column in range(W):
                color = pixel_values[iter]
                iter += 1
                myImage.set_value(row, column, Color(color[0], color[1], color[2]))
        images.append(myImage)
    return Slides(W, H, images)




if __name__ == '__main__':
    def get_args():
        parser = argparse.ArgumentParser()
        parser.add_argument('-H', type=int, default=20)
        parser.add_argument('-W', type=int, default=20)
        parser.add_argument('--iter', '-i', type=int, default=5)
        parser.add_argument('--refresh', '-r', type=float, default=0.1)
        files = parser.add_mutually_exclusive_group(required=True)
        files.add_argument('--dir', type=str)
        files.add_argument('--gif', type=str)
        options = parser.parse_args()
        return options
    options = get_args()
    if options.dir is not None:
        slides = dir_to_slides(options.dir, W=options.W, H=options.H)
        slideshow(slides, iterations=options.iter, refresh=options.refresh)
    if options.gif is not None:
        slides = gif_to_slides(options.gif, W=options.W, H=options.H)
        slideshow(slides, iterations=options.iter, refresh=options.refresh)

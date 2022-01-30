from PIL import Image
import colorama
import time
from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

image_path = input('Print your image path:  ')


class Loader:
    def __init__(self, desc="Loading...", end=' '*110 + "Done!", timeout=0.1):
        self.desc = desc
        self.end = end
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for c in cycle(self.steps):
            if self.done:
                break
            print(f"\r{self.desc} {c}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        self.stop()


if __name__ == "__main__":
    for i in range(5):
        print()
    with Loader(' '*110 + "Loading with context manager..."):
        for i in range(10):
            sleep(0.25)

    loader = Loader(' '*110 + "Loading with object...", ' '*110 + "That was fast!"+'\n'*5, 0.05).start()
    for i in range(10):
        sleep(0.25)
    loader.stop()

colorama.init()


class AsciiArt:
    def __init__(self, image_path):
        self.path = image_path
        self.img = Image.open(self.path)

    def image(self):
        width, height = self.img.size
        aspect_ratio = height/width
        new_width = 120
        new_height = aspect_ratio * new_width * 0.55
        img = self.img.resize((new_width, int(new_height)))
        img = img.convert('L')
        pixels = img.getdata()
        chars = ["@", "#", "S", "$", "?", "*", "+", ";", ":", ",", "."]
        new_pixels = [chars[pixel//25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)
        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width]
                       for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        file = "ascii_image.txt"
        with open(file, 'w') as f:
            f.write(ascii_image)

        x = 0
        print(' '*60, end='')
        for pix in ascii_image:
            time.sleep(0.0002)
            if x == new_width:
                print()
                print(' '*60, end='')
                x = 0
            else:

                print(pix, end='')
                x += 1
        for i in range(5):
            print()


if __name__ == "__main__":
    AsciiArt(image_path).image()
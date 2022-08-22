# -*- coding: utf-8 -*-
from django import VERSION as DJANGO_VERSION

from PIL import Image


def get_image_background_color(img, alpha=False):
    w,h = img.size
    width = w/2
    height= h/1.5
    img = img.convert("RGBA" if alpha else "RGB")
    pixel_color = img.getpixel((width, height))
    color_format = "#" + "%02x" * len(pixel_color)
    color = color_format % pixel_color
    color = color.upper()
    return color


def get_image_file_background_color(img_file, alpha=False):

    color = ""
    with Image.open(img_file) as image:
        color = get_image_background_color(image, alpha)
    return color

def _get_image_field_color(self):
        color = ""
        if self.image:
            image_file= self.image
        else:
            image_file = self.product.image
        
        
        if image_file:
            alpha = "hexa"
            if DJANGO_VERSION >= (2, 0):
                # https://stackoverflow.com/a/3033986/2096218
               
                    color = get_image_file_background_color(image_file, alpha)
            else:
                # https://stackoverflow.com/a/3033986/2096218
                color = get_image_file_background_color(image_file, alpha)
        return color
        
   

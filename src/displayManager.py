#!/usr/bin/python3
# -*- coding:utf-8 -*-
import os
import logging

from . import epd7in5_V2

from PIL import Image,ImageDraw,ImageFont

epd = epd7in5_V2.EPD()

logging.basicConfig(level=logging.DEBUG)

class DisplayManager:
    COLOR_MAP = {
        'black': (0,0,0),
        'white': (255,255,255),
        'gray': (128,128,128),
        'light-gray': (180,180,180)
    }

    __location__ = os.path.realpath(
        os.path.join(
            os.getcwd(),
            os.path.dirname(
                __file__
            )
        )
    )


    def __init__(self, image_width=epd.width, image_height=epd.height):
        self.image = Image.new('RGB', (image_width, image_height), (255,255,255))
        self.draw = ImageDraw.Draw(self.image)

    def draw_progress_bar(self, progress, x, y, bar_width, bar_height, padding=4, background_color='black', bar_fill_color='gray', border_color='black', border_width=4):
        logging.debug("Calculating progress size")
        filled_width = int((progress / 100) * (bar_width - 2 * padding))

        logging.info("Drawing border of bar background")
        background_coords = [(x + padding - border_width, y + padding - border_width),
                             (x + bar_width - padding + border_width - 1, y + bar_height - padding + border_width - 1)]
        self.draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=self.COLOR_MAP.get(background_color, (0,0,0)), outline=self.COLOR_MAP.get(border_color, (0,0,0)), width=border_width)

        logging.info("Drawing background of progress bar")
        background_coords = [(x + padding, y + padding), (x + bar_width - padding - 1, y + bar_height - padding - 1)]
        self.draw.rounded_rectangle(background_coords, radius=(bar_height - 2 * padding) // 2, fill=self.COLOR_MAP.get(background_color, (0,0,0)))

        logging.info("Drawing progress bar")
        filled_coords = [(x + padding, y + padding), (x + filled_width + padding, y + bar_height - padding - 1)]
        self.draw.rounded_rectangle(filled_coords, radius=(bar_height - 2 * padding) // 2, fill=self.COLOR_MAP.get(bar_fill_color, (128,128,128)))
    
    def draw_text(self, text, x, y, fontSize=32, fontPath=None):
        logging.debug("Setting default font")
        if fontPath is None:
            fontPath = self.__location__ + '/font/Asap/Asap-VariableFont_wdth,wght.ttf'
        logging.info("Drawing text")
        font = ImageFont.truetype(fontPath, size=fontSize)
        text_x = x
        text_y = y
        self.draw.text((text_x, text_y), text, font=font, fill=(0, 0, 0))
    
    def draw_line(self, start_coords, end_coords, color=(0,0,0), width=2):
        logging.info("Drawing line")
        self.draw.line([start_coords, end_coords], fill=color, width=width)
    
    def draw_box(self, start_coords, end_coords, radius, fill_color='light-gray'):
        logging.info("Drawing rounded rectangle")
        self.draw.rounded_rectangle([start_coords, end_coords], radius, self.COLOR_MAP.get(fill_color, (180,180,180)))

    def display_image(self):
        try:
            logging.info("Initializing and clearing EPD")
            epd = epd7in5_V2.EPD()
            epd.init()
            epd.Clear()

            logging.info("Drawing image")
            epd.display(epd.getbuffer(self.image))

            logging.info("Set display to sleep")
            epd.sleep()

        except IOError as e:
            logging.info(e)

        except KeyboardInterrupt:    
            logging.info("ctrl + c:")
            epd7in5_V2.epdconfig.module_exit()
            exit()
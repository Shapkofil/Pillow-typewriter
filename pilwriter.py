#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import cv2

import numpy as np
import subprocess
import random

from tqdm import tqdm

import argparse

parser = argparse.ArgumentParser(description='Recording Parameters')
parser.add_argument('source', help="Text to be writen out")
parser.add_argument("-o", "--output", default="pilwriter", help="Only name is needed here. The MKV format is hard coded")
parser.add_argument("-f", "--framerate", default=24)
parser.add_argument("-s", "--fontsize", default=24)

args = parser.parse_args()

raw_text = "The hall of the example"


class PilWriter():
    def __init__(self,
                 text="",
                 img_size=(1920, 1080),
                 font="SourceCodePro-Bold.otf",
                 font_size=20):

        self.fnt = ImageFont.truetype(font, font_size)
        self.img_size = img_size


        if not text == "":
            text = " ".join(text.split("\n"))
            text = "\n".join(textwrap.wrap(text, img_size[0]//(font_size*1.33333)))
            print("weird {}".fromat(img_size[0]//(font_size*1.33333)))
            self.mstates = [text[:end] for end in range(len(text)+1)]
            self.text = text


    def gen_img(self, text, linespacing=1.5):
        text_mask = Image.new("L", self.img_size, 0)
        d = ImageDraw.Draw(text_mask)
        w, h = d.textsize(text, font=self.fnt)
        d.text(((self.img_size[0] - w) / 2, (self.img_size[1] - h) / 2),
               text,
               fill=255,
               font=self.fnt,
               align="left")

        self.img = text_mask
        return self.img

    def gen_video(self, video_name="pilwriter", linespacing=1.5, framerate=24):
        subprocess.call("mkdir {}tmp".format(video_name).split())

        for i,state in enumerate(tqdm(self.mstates)):
            self.gen_img(state, linespacing).save("{1}tmp/{0}.png".format(i,video_name))


        subprocess.call("ffmpeg -framerate {1} -i {0}tmp/%d.png -codec copy {0}.mkv".format(video_name, framerate).split())
        subprocess.call("rm -rf {}tmp".format(video_name).split())



if __name__ == "__main__":
    writer = PilWriter(text=args.source, font_size=int(args.fontsize))
    writer.gen_video(args.output, args.framerate)

# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
# get an image
base = Image.open('captcha.jpg').convert('RGBA')

# make a blank image for the text, initialized to transparent text color
txt = Image.new('RGBA', base.size, (255,255,255,0))

# get a font
fnt = ImageFont.truetype('msyh.ttf', 20)
# get a drawing context
d = ImageDraw.Draw(txt)

# draw text, half opacity
d.text((10,10), "你好你好你好你好你好", font=fnt, fill=(0,0,0,255))
# draw text, full opacity
d.text((10,40), "顾为你好你好你好你好你好", font=fnt, fill=(0,0,0,255))

out = Image.alpha_composite(base, txt)

out.show()
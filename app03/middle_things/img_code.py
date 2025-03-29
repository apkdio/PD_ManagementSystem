import random

from PIL import Image, ImageDraw, ImageFont


def code_img():
    img = Image.new(mode="RGB", size=(120, 30), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode="RGB")
    x, y = random.randint(0, 5), random.randint(0, 5)
    Aa=[65,97]
    str = ""
    # 写字母
    for i in range(random.randint(2, 4)):
        choice=random.choice(Aa)
        s = chr(random.randint(choice,choice+25))
        block = random.randint(0, 3) * " "
        str += block + s
    r = random.randint(200, 255)
    g = random.randint(0, 50)
    b = random.randint(0, 255)
    draw.text([x, y], str,
              fill=(r, g, b),
              font=ImageFont.truetype("C:/Users/Administrator/PycharmProjects/example01/app03/middle_things/font/hy.ttf", 20))
    # 干扰点
    for i in range(60):
        draw.point((random.randint(0, 120), random.randint(0, 30)),
                   fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    # 干扰线
    for i in range(12):
        x1 = random.randint(0, 20)
        x2 = random.randint(0, 120)
        y1 = random.randint(5, 30)
        y2 = random.randint(0, 30)
        draw.line([(x1, y1), (x2, y2)],
                  fill=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))

    return img, "".join(str.replace(" ", ""))

from PIL import Image, ImageDraw, ImageFont
import os

def read_txt(id):
    lines = []
    result = []
    with open('ark-results/' + id + '.txt.txt', 'r') as f:
        lines = f.readlines()
    del lines[-1]
    lines = [line.replace('\n', '').split('\t') for line in lines]
    print lines
    for item in lines:
        if float(item[-1]) > 0.75:
            result.append(item[0])
    return result

def tag():
    dirs = os.listdir('py3/photos')
    results = os.listdir('ark-results')
    for d in dirs:
        pics = os.listdir('py3/photos/' + d)
        for pic in pics:
            id = pic[:pic.find('.')]
            words = read_txt(id)
            img = Image.open('py3/photos/' + d + '/' + pic)
            rgb_im = img.convert('RGB')
            r, g, b = rgb_im.getpixel((0, 0))
            draw = ImageDraw.Draw(img)
            font = ImageFont.truetype("micross.ttf", 30)
            pos = 0
            for i in words:
                draw.text((0, pos), i ,(255-r,255-g,255-b), font=font)
                pos += 30
            img.save('tagged_pic/' + pic)

if __name__ == "__main__":
    tag()

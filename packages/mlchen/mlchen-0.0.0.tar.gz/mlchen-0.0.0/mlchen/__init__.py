import os
import time
import random

# import cv2
from PIL import Image
    
def read_image(image_path, method="opencv"):
    if method == "pillow":
        img = Image.open(image_path)
        grey_image = img.convert("L")
    # elif method == "opencv":
    #     img = cv2.imread(image_path)
    #     grey_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return grey_image

STANDARD_CHAR_LIST = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^'\`. ")
ABBREVIATED_CHAR_LIST = list("@%#*+=-:. ")

def img2ascii(grey_image, char_list=ABBREVIATED_CHAR_LIST, scale=1.0, method='pillow'):
    if method == 'pillow':
        scaled_img_width = int(grey_image.size[0] * scale) # 按比例放大或缩小图片
        scaled_img_height = int(grey_image.size[1] * scale)
        scaled_grey_img = grey_image.resize((scaled_img_width, scaled_img_height))
    # elif method == 'opencv':
    #     scaled_grey_img = cv2.resize(grey_image, None, fx=scale, fy=scale)
    #     scaled_img_width = len(scaled_grey_img[0])
    #     scaled_img_height = len(scaled_grey_img)
    char_list_length = len(char_list)
    ascii_img = [[None for i in range(scaled_img_width)] for j in range(scaled_img_height)]
    ascii_color = [x[:] for x in ascii_img]
    for i in range(scaled_img_height):
        for j in range(scaled_img_width):
            if method == "pillow":
                # brightness: the larger, the brighter, and later position in given char list
                brightness = scaled_grey_img.getpixel((j, i))
            elif method == "opencv":
                brightness = scaled_grey_img[i, j]
            brightness = 255 - brightness
            ascii_img[i][j] = char_list[int(brightness * char_list_length / 255) % len(char_list)]
    return ascii_img


ANSI_BLACK = 30
ANSI_RED = 31
ANSI_GREEN = 32
ANSI_YELLOW = 33
ANSI_BLUE= 34
ANSI_PURPLE = 35
ANSI_CYAN = 36
ANSI_WHITE = 37

ANSI_BLACK_BACKGROUND = 40
ANSI_RED_BACKGROUND = 41
ANSI_GREEN_BACKGROUND = 42
ANSI_YELLOW_BACKGROUND = 43
ANSI_BLUE_BACKGROUND= 44
ANSI_PURPLE_BACKGROUND = 45
ANSI_CYAN_BACKGROUND = 46
ANSI_WHITE_BACKGROUND= 47

MOD_DEFAULT= 0
MOD_HIGHLIGHT = 1
MOD_UNDERLINE = 4
MOD_FLICKER = 5
MOD_INVERSE = 7
MOD_HIDE = 8

def mode_print(msg, fg=ANSI_WHITE, bg=ANSI_BLACK_BACKGROUND, mod=MOD_DEFAULT):
    print('\033[{};{};{}m'.format(fg,bg,mod) + msg + '\033[0m')


def lulu_talks():
    print('Emm? Who is there? BabyTong?')


def lulu_says_love():
    
    # sentence = 'I Love You BabyTong'
    # for c in sentence.split():
    #     allChar = []
    #     for y in range(12, -12, -1):
    #         lst = []
    #         lst_con = ''
    #         for x in range(-30,30):
    #             formula = ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3
    #             if formula <= 0:
    #                 lst_con += c[(x) % len(c)]
    #             else:
    #                 lst_con += ' '
    #         lst.append(lst_con)
    #         allChar += lst
    #     print('\n'.join(allChar))
    #     time.sleep(1)

    sentence = 'I-Love-You-BabyTong-'
    allChar = []
    for y in range(12, -12, -1):
        lst = []
        lst_con = ''
        for x in range(-30,30):
            formula = ((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3
            if formula <= 0:
                lst_con += sentence[(x) % len(sentence)]
            else:
                lst_con += ' '
        lst.append(lst_con)
        allChar += lst
    # mode_print('\n'.join(allChar), ANSI_RED, ANSI_BLACK_BACKGROUND, MOD_DEFAULT)
    print('\n'.join(allChar))
    

def lulu_what_should_i_eat_today():
    dishes = [
        r'青椒炒肉丝', r'黄焖鸡米饭', r'先进院一楼麻辣烫', r'先进院六楼鲮鱼麦菜',
        r'点外卖胖哥俩肉蟹煲', r'湖南小炒肉', r'点外卖轻食', r'先进院二楼面食',
        r'宫保鸡丁']
    print(random.choice(dishes))


def lulu_draws():

    image = read_image(
        os.path.join(os.path.dirname(__file__), 'drawing.jpg'), method='pillow')
    ascii_image = img2ascii(image, method='pillow')

    text = ''
    for row in ascii_image:
        for c in row:
            text += (c+' ')
        text += '\n'
    # text = [ for row in ascii_image]
    print(text)
from PIL import Image, ImageDraw, ImageFont
import math
import os
import string

def str_count(str):
    '''找出字符串中的中英文、空格、数字、标点符号个数'''
    count_en = count_dg = count_sp = count_zh = count_pu = 0
    
    for s in str:
        # 英文
        if s in string.ascii_letters:
            count_en += 1
        # 数字
        elif s.isdigit():
            count_dg += 1
        # 空格
        elif s.isspace():
            count_sp += 1
        # 中文
        elif s.isalpha():
            count_zh += 1
        # 特殊字符
        else:
            count_pu += 1
    print('英文字符：', count_en)
    print('数字：', count_dg)
    print('空格：', count_sp)
    print('中文：', count_zh)
    print('特殊字符：', count_pu)
    return count_en, count_dg, count_sp, count_zh, count_pu

def make_text_image(width, white, text, save_path, mode="rgb"):
    """
    生成一个文字图形, white=1，表示白底黑字，否则为黑底白字
    """
    
    # 字体可能要改
    # linux查看支持的汉字字体 # fc-list :lang=zh
    ft = ImageFont.truetype("C:\Windows\Fonts\msyhbd.ttc", 35)
    w, h = ft.getsize(text)
    
    # 计算要几行
    lines = math.ceil(w / width) + 1
    height = h * lines
    
    # 一个汉字的宽度
    one_zh_width, h = ft.getsize("中")
    one_en_width, h = ft.getsize("V")
    one_ch_width, h = ft.getsize(".")
    one_num_width, h = ft.getsize("9")
    
    if len(mode) == 1:  # L, 1
        background = (255)
        color = (0)
    if len(mode) == 3:  # RGB
        background = (255, 255, 255)
        color = (0, 0, 0)
    if len(mode) == 4:  # RGBA, CMYK
        background = (255, 255, 255, 255)
        color = (0, 0, 0, 0)
    
    newImage = Image.new(mode, (width, height), background if white else color)
    draw = ImageDraw.Draw(newImage)
    
    # 分割行
    if len(text) > 15:
        text = text + " "  # 处理最后少一个字问题
        text_list = []
        start = 0
        end = len(text) - 1
        while start < end:
            for n in range(end):
                try_text = text[start:start + n]
                w, h = ft.getsize(try_text)
                if w + 2 * one_zh_width > width:
                    break
            text_list.append(try_text[0:-1])
            start = start + n - 1;
    
        # print(text_list)
        i = 0
        for t in text_list:
            draw.text((one_zh_width, i * h), t, color if white else background, font=ft)
            i = i + 1
    else:
        en, num, sp, zh, ch = str_count(text)
        w = (width - en*one_en_width - num*one_num_width - sp*1 - zh*one_zh_width - ch*one_ch_width)/2
        draw.text((w, 0), text, color if white else background, font=ft)
        # draw.text((one_zh_width, 0), text, color if white else background, font=ft)
        
    newImage.save(save_path);


def resize_canvas(new_image_path="生成结果.jpg"):
    dir_path = os.path.dirname(os.path.abspath(__file__))
    print('当前目录绝对路径:', dir_path)
    org_image = input("Please input the org_image file with path")
    # add_image = dir_path + '\tmp.png'
    add_image = 'tmp.png'
    
    org_im = Image.open(org_image)
    org_width, org_height = org_im.size
    
    mode = org_im.mode
    text = input("Please input the text")
    make_text_image(org_width, 1, text, add_image, mode)
    
    add_im = Image.open(add_image)
    add_width, add_height = add_im.size
    
    mode = org_im.mode
    
    newImage = Image.new(mode, (org_width, org_height + add_height))
    
    newImage.paste(org_im, (0, 0, org_width, org_height))
    newImage.paste(add_im, (0, org_height, add_width, add_height + org_height))
    newImage.save(new_image_path)


resize_canvas()

# def addText(img, string):
#     font = ImageFont.truetype("C:\Windows\Fonts\Arial.ttf", 24)
#     size = img.size
#     width = size[0] - 20
#     high = size[1] - 20
#     lenth = len(string) * 3
#     draw = ImageDraw.Draw(img)
#     draw.text((width - lenth, high), string, fill='black', font=font)
#     oriImg.show()
#     oriImg.save(path)


# path = input("Please input the image file with path")
#
# try:
#     print("path: " + path)
#     oriImg = Image.open(path)
#     addText(oriImg, "good")
# except IOError:
#     print("can't' open the file,check the path again")
#     newImg = Image.new('RGBA', (320, 240), 'white')
#     newImg.save(path)
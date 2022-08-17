import cv2
import os
from PIL import Image, ImageDraw, ImageFont

# 阿拉伯数字转汉字
_MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四', u'十五', u'十六', u'十七',u'十八', u'十九')
_P0 = (u'', u'十', u'百', u'千',)
_S4 = 10 ** 4
def to_chinese(num):
    assert (0 <= num and num < _S4)
    if num < 20:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
        return result[::-1]

# 裁剪图片并保存
def reSize(img):
    img1 = img[5:514, 7:430] # 左半边
    cv2.imwrite("D:/test1.jpg", img1)
    img2 = img[5:514, 392:815] # 右半边
    cv2.imwrite("D:/test2.jpg", img2)

# 添加页码
myfont = ImageFont.truetype("./FZYingXueJW.TTF", 20)

def addColText(draw, left, top, text, font):
    for i in range(0, len(text)):
        draw.text((left, top), text[i], (0, 0, 0), font)
        top += 20

def addSubL(img, num):
    draw = ImageDraw.Draw(img)
    addColText(draw, 394, 170, to_chinese(num), myfont)
    img.save("D:/test11.jpg")

def addSubR(img, num):
    draw = ImageDraw.Draw(img)
    addColText(draw, 10, 170, to_chinese(num), myfont)
    img.save("D:/test22.jpg")

def reSize2(img):
    p = 1748 / 423
    img = cv2.resize(img, (0,0), fx=p, fy=p)
    cv2.imwrite('./test.jpg', img)

# 放到A5
def toA5(img, out):
    reSize2(img)
    bg = Image.open('./bg.jpg')
    bg.convert('RGBA')
    icon = Image.open('./test.jpg')
    bg.paste(icon, (0, 192), mask=None)
    bg.save(out)

if __name__ == '__main__':
    rootdir = 'D:/in'
    count = 1
    p = 1
    list1 = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
    print("共{}张图片".format(len(list1)))
    for i in range(0, len(list1)):
        path = os.path.join(rootdir, list1[i])
        if os.path.isfile(path):
            img = cv2.imread(path)
            reSize(img)
            addSubR(Image.open('D:/test2.jpg'), count)
            addSubL(Image.open('D:/test1.jpg'), count+1)
            toA5(cv2.imread('D:/test22.jpg'), "D:/out/%d.jpg"%(count))
            toA5(cv2.imread('D:/test11.jpg'), "D:/out/%d.jpg"%(count+1))
            count += 2
        print("已完成{}张".format(p))
        p += 1
            


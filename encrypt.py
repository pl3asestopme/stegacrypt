from PIL import Image, ImageDraw
from random import randint


def stega_encrypt():
    keys = []  # сюда будут помещены ключи
    img = Image.open(input("Изображение: "))  # создаём объект изображения
    draw = ImageDraw.Draw(img)  # объект рисования
    width = img.size[0]  # ширина
    height = img.size[1]  # высота
    pix = img.load()  # все пиксели тут
    f = open('keys.txt', 'w')  # текстовый файл для ключей

    for elem in ([ord(elem) for elem in input("Введите текст, который нужно зашифровать: ")]):
        key = (randint(1, width - 10), randint(1, height - 10))
        g, b = pix[key][1:3]
        draw.point(key, (elem, g, b))
        f.write(str(key) + '\n')

    print('Ключи шифрования были записаны в  keys.txt')
    print('Текст зашифрованный в изображении называется newimage.png')
    img.save("newimage.png", "png")
    f.close()


stega_encrypt()

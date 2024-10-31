from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from PIL import Image, ImageDraw
import os

# Загрузка открытого ключа
def load_public_key(file_name):
    with open(file_name, 'rb') as key_file:
        public_key = serialization.load_pem_public_key(key_file.read())
    return public_key

# Шифрование сообщения с использованием открытого ключа
def encrypt_message(message, public_key):
    ciphertext = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext

def select_image():
    images = [f for f in os.listdir() if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif'))]
    
    if not images:
        print("Нет доступных изображений в каталоге.")
        return None

    print("Доступные изображения:")
    for idx, img in enumerate(images):
        print(f"{idx + 1}: {img}")

    while True:
        choice = input("Введите номер изображения для выбора или 'q' для выхода: ")
        if choice.lower() == 'q':
            return None
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(images):
                return images[choice_idx]
            else:
                print("Некорректный номер изображения. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def select_public_key():
    public_keys = [f for f in os.listdir() if f.endswith('_public.key')]
    
    if not public_keys:
        print("Нет доступных открытых ключей в каталоге.")
        return None

    print("Доступные открытые ключи:")
    for idx, key in enumerate(public_keys):
        print(f"{idx + 1}: {key}")

    while True:
        choice = input("Введите номер открытого ключа для шифрования или 'q' для выхода: ")
        if choice.lower() == 'q':
            return None
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(public_keys):
                return public_keys[choice_idx]
            else:
                print("Некорректный номер ключа. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def stega_encrypt():
    try:
        image_name = select_image()  # выбор изображения
        if not image_name:
            return  # Выход, если изображение не выбрано

        public_key_file = select_public_key()  # выбор открытого ключа
        if not public_key_file:
            return  # Выход, если открытый ключ не выбран
        public_key = load_public_key(public_key_file)  # Загружаем выбранный открытый ключ
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    text = input("Введите текст, который нужно зашифровать: ")
    encrypted_text = encrypt_message(text, public_key)

    img = Image.open(image_name)  # создаём объект изображения
    draw = ImageDraw.Draw(img)  # объект рисования
    width, height = img.size  # ширина и высота

    # Сохраняем длину шифротекста в изображении
    length_bytes = len(encrypted_text).to_bytes(2, byteorder='big')
    
    # Сохраняем длину шифротекста в первых двух пикселях
    draw.point((0, 0), (length_bytes[0], 0, 0))
    draw.point((0, 1), (length_bytes[1], 0, 0))

    # Сохраняем каждый байт зашифрованного текста в изображении
    for idx, byte in enumerate(encrypted_text):
        x = (idx % width)
        y = (idx // width) + 2  # Сохраняем с третьей строки
        draw.point((x, y), (byte, 0, 0))

    # Сохранение нового изображения с тем же расширением
    new_image_name = input("Введите имя для сохраненного изображения (без расширения): ") or f"{image_name.split('.')[0]}_encrypted"
    img.save(f"{new_image_name}.{image_name.split('.')[-1]}", "png")
    print(f"Текст зашифрованный в изображении называется {new_image_name}.{image_name.split('.')[-1]}")

if __name__ == "__main__":
    stega_encrypt()

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from PIL import Image
import os

# Загрузка закрытого ключа
def load_private_key(file_name):
    with open(file_name, 'rb') as key_file:
        private_key = serialization.load_pem_private_key(key_file.read(), password=None)
    return private_key

# Дешифрование сообщения с использованием закрытого ключа
def decrypt_message(ciphertext, private_key):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode()

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

def select_private_key():
    private_keys = [f for f in os.listdir() if f.endswith('_private.key')]
    
    if not private_keys:
        print("Нет доступных закрытых ключей в каталоге.")
        return None

    print("Доступные закрытые ключи:")
    for idx, key in enumerate(private_keys):
        print(f"{idx + 1}: {key}")

    while True:
        choice = input("Введите номер закрытого ключа для расшифровки или 'q' для выхода: ")
        if choice.lower() == 'q':
            return None
        try:
            choice_idx = int(choice) - 1
            if 0 <= choice_idx < len(private_keys):
                return private_keys[choice_idx]
            else:
                print("Некорректный номер ключа. Попробуйте снова.")
        except ValueError:
            print("Пожалуйста, введите число.")

def decrypt_text(image_name):
    img = Image.open(image_name)
    pix = img.load()
    width, height = img.size

    # Извлечение длины шифротекста
    length_bytes = bytearray()
    length_bytes.append(pix[0, 0][0])
    length_bytes.append(pix[0, 1][0])
    ciphertext_length = int.from_bytes(length_bytes, byteorder='big')

    print(f"Длина шифротекста: {ciphertext_length}")

    # Извлечение шифротекста из изображения
    encrypted_bytes = bytearray()
    for idx in range(ciphertext_length):
        x = idx % width
        y = (idx // width) + 2  # Начинаем с третьей строки
        encrypted_bytes.append(pix[x, y][0])

    print(f"Извлеченный шифротекст: {list(encrypted_bytes)}")  # Отладочная информация

    # Дешифруем сообщение
    private_key_file = select_private_key()  # выбор закрытого ключа
    if not private_key_file:
        return  # Выход, если закрытый ключ не выбран
    private_key = load_private_key(private_key_file)  # Загружаем выбранный закрытый ключ
    
    try:
        decrypted_text = decrypt_message(bytes(encrypted_bytes), private_key)
        print(f"Текст, который был расшифрован: {decrypted_text}")
    except Exception as e:
        print(f"Не удалось расшифровать сообщение: {e}")

if __name__ == "__main__":
    image_name = select_image()  # выбираем изображение
    if image_name:
        decrypt_text(image_name)  # Дешифруем текст из выбранного изображения

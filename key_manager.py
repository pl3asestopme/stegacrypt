from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend
import os

def generate_keys(user_name):
    # Создаём имена файлов на основе имени пользователя
    private_key_file = f"{user_name}_private.key"
    public_key_file = f"{user_name}_public.key"
    
    # Проверка существования ключей
    if os.path.exists(private_key_file) and os.path.exists(public_key_file):
        print(f"Ключи для '{user_name}' уже существуют: {private_key_file} и {public_key_file}")
        overwrite = input("Перезаписать существующие ключи? (y/n): ").strip().lower()
        if overwrite != 'y':
            print("Ключи не были перезаписаны.")
            return
    
    # Генерация пары ключей
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Сохранение закрытого ключа
    with open(private_key_file, "wb") as private_file:
        private_file.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

    # Сохранение открытого ключа
    with open(public_key_file, "wb") as public_file:
        public_file.write(
            public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )

    print(f"Ключи для '{user_name}' успешно сгенерированы и сохранены как {private_key_file} и {public_key_file}")

if __name__ == "__main__":
    user_name = input("Введите имя пользователя для генерации ключей: ")
    generate_keys(user_name)

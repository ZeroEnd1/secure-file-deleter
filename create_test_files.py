"""
Скрипт для створення тестових файлів для експериментів
Створює текстові та графічні файли розміром ≥512 КБ
"""

import os
import sys
import random
from PIL import Image, ImageDraw, ImageFont

# Налаштування кодування для Windows консолі
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

def create_text_file(filename, size_kb=512):
    """
    Створити текстовий файл заданого розміру
    
    Args:
        filename: Ім'я файлу
        size_kb: Розмір файлу в кілобайтах (за замовчуванням 512 КБ)
    """
    size_bytes = size_kb * 1024
    
    # Генерація випадкового тексту
    text_content = []
    current_size = 0
    
    sample_text = (
        "Це тестовий файл для експерименту з безпечним видаленням файлів. "
        "Програма використовує алгоритм German VSITR для остаточного видалення даних. "
        "Алгоритм виконує 7 проходів перезапису: 0x00, 0xFF, псевдовипадкові дані (3 проходи), "
        "0xAA, та знову псевдовипадкові дані. "
    )
    
    while current_size < size_bytes:
        line = f"[Рядок {len(text_content) + 1}] {sample_text}\n"
        text_content.append(line)
        current_size += len(line.encode('utf-8'))
    
    # Запис у файл
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(text_content)
    
    actual_size = os.path.getsize(filename)
    print(f"[OK] Створено текстовий файл: {filename}")
    print(f"  Розмір: {actual_size / 1024:.2f} КБ ({actual_size} байт)")


def create_image_file(filename, size_kb=512):
    """
    Створити графічний файл заданого розміру
    
    Args:
        filename: Ім'я файлу
        size_kb: Мінімальний розмір файлу в кілобайтах
    """
    # Розрахунок розмірів зображення для досягнення потрібного розміру файлу
    # PNG з високою якістю: приблизно 3-4 байти на піксель
    target_pixels = (size_kb * 1024) // 3
    width = int((target_pixels ** 0.5) * 1.5)
    height = int(target_pixels / width)
    
    # Створення зображення з випадковими кольоровими блоками
    image = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(image)
    
    # Малювання випадкових кольорових прямокутників
    block_size = 50
    for x in range(0, width, block_size):
        for y in range(0, height, block_size):
            color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            )
            draw.rectangle(
                [x, y, x + block_size, y + block_size],
                fill=color,
                outline='black'
            )
    
    # Додавання тексту
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    
    text = "TEST FILE FOR SECURE DELETION"
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Тінь тексту
    draw.text((text_x + 2, text_y + 2), text, fill='black', font=font)
    # Основний текст
    draw.text((text_x, text_y), text, fill='white', font=font)
    
    # Збереження з високою якістю
    image.save(filename, 'PNG', optimize=False)
    
    actual_size = os.path.getsize(filename)
    print(f"[OK] Створено графічний файл: {filename}")
    print(f"  Розмір: {actual_size / 1024:.2f} КБ ({actual_size} байт)")
    print(f"  Розміри: {width}x{height} пікселів")


def create_readonly_file(filename, size_kb=512):
    """
    Створити файл тільки для читання
    
    Args:
        filename: Ім'я файлу
        size_kb: Розмір файлу в кілобайтах
    """
    create_text_file(filename, size_kb)
    
    # Зробити файл тільки для читання
    import stat
    os.chmod(filename, stat.S_IREAD)
    
    print(f"[OK] Файл {filename} встановлено як 'тільки для читання'")


def main():
    """Створення всіх тестових файлів"""
    print("=" * 60)
    print("Створення тестових файлів для експериментів")
    print("=" * 60)
    print()
    
    # Створення директорій для експериментів
    os.makedirs("experiment_1_unsafe", exist_ok=True)
    os.makedirs("experiment_2_secure", exist_ok=True)
    os.makedirs("backup_copies", exist_ok=True)
    
    print("Експеримент 1: Небезпечне видалення (Shift+Delete)")
    print("-" * 60)
    
    # Файли для експерименту 1
    create_text_file("experiment_1_unsafe/test_text_unsafe.txt", 512)
    create_image_file("experiment_1_unsafe/test_image_unsafe.png", 512)
    
    # Резервні копії для експерименту 1
    create_text_file("backup_copies/test_text_unsafe_backup.txt", 512)
    create_image_file("backup_copies/test_image_unsafe_backup.png", 512)
    
    print()
    print("Експеримент 2: Безпечне видалення (German VSITR)")
    print("-" * 60)
    
    # Файли для експерименту 2
    create_text_file("experiment_2_secure/test_text_secure.txt", 512)
    create_image_file("experiment_2_secure/test_image_secure.png", 512)
    
    # Резервні копії для експерименту 2
    create_text_file("backup_copies/test_text_secure_backup.txt", 512)
    create_image_file("backup_copies/test_image_secure_backup.png", 512)
    
    print()
    print("Додаткове завдання: Файл тільки для читання")
    print("-" * 60)
    
    # Файл тільки для читання
    create_readonly_file("experiment_2_secure/test_readonly.txt", 512)
    create_text_file("backup_copies/test_readonly_backup.txt", 512)
    
    print()
    print("=" * 60)
    print("[OK] Всі тестові файли успішно створено!")
    print("=" * 60)
    print()
    print("Структура файлів:")
    print("  experiment_1_unsafe/")
    print("    ├── test_text_unsafe.txt (для Shift+Delete)")
    print("    └── test_image_unsafe.png (для Shift+Delete)")
    print()
    print("  experiment_2_secure/")
    print("    ├── test_text_secure.txt (для програми)")
    print("    ├── test_image_secure.png (для програми)")
    print("    └── test_readonly.txt (тільки для читання)")
    print()
    print("  backup_copies/")
    print("    └── (резервні копії всіх файлів)")
    print()


if __name__ == "__main__":
    main()
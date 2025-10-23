"""
Secure File Deleter - German VSITR Algorithm Implementation
Десктопна програма для остаточного видалення файлів
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import random
import stat
import string
from pathlib import Path
import logging
from datetime import datetime

# Налаштування логування
logging.basicConfig(
    filename='secure_delete_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)


class SecureFileDeleter:
    """Клас для безпечного видалення файлів за алгоритмом German VSITR"""
    
    def __init__(self):
        self.passes = [
            ('0x00', b'\x00'),  # Прохід 1
            ('0xFF', b'\xFF'),  # Прохід 2
            ('Random 1', None), # Прохід 3
            ('Random 2', None), # Прохід 4
            ('Random 3', None), # Прохід 5
            ('0xAA', b'\xAA'),  # Прохід 6
            ('Random 4', None)  # Прохід 7
        ]
    
    def make_writable(self, filepath):
        """Зробити файл доступним для запису (для файлів тільки для читання)"""
        try:
            os.chmod(filepath, stat.S_IWRITE | stat.S_IREAD)
            logging.info(f"Змінено атрибути файлу: {filepath}")
            return True
        except Exception as e:
            logging.error(f"Помилка зміни атрибутів: {e}")
            return False
    
    def overwrite_file(self, filepath, data_byte, file_size, progress_callback=None):
        """Перезаписати файл заданими даними"""
        try:
            with open(filepath, 'rb+') as f:
                chunk_size = 4096  # 4 KB chunks
                written = 0
                
                while written < file_size:
                    remaining = file_size - written
                    current_chunk = min(chunk_size, remaining)
                    
                    if data_byte is None:  # Псевдовипадкові дані
                        chunk = bytes(random.randint(0, 255) for _ in range(current_chunk))
                    else:
                        chunk = data_byte * current_chunk
                    
                    f.write(chunk)
                    written += current_chunk
                    
                    if progress_callback:
                        progress = (written / file_size) * 100
                        progress_callback(progress)
                
                f.flush()
                os.fsync(f.fileno())
            
            return True
        except Exception as e:
            logging.error(f"Помилка перезапису файлу: {e}")
            return False
    
    def rename_file_randomly(self, filepath, times=3):
        """Перейменувати файл випадковими іменами"""
        current_path = Path(filepath)
        parent_dir = current_path.parent
        
        try:
            for i in range(times):
                # Генерація випадкового імені
                random_name = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
                new_path = parent_dir / random_name
                
                os.rename(current_path, new_path)
                logging.info(f"Перейменовано: {current_path.name} -> {new_path.name}")
                current_path = new_path
            
            return str(current_path)
        except Exception as e:
            logging.error(f"Помилка перейменування: {e}")
            return str(current_path)
    
    def secure_delete(self, filepath, progress_callback=None, status_callback=None):
        """
        Безпечне видалення файлу за алгоритмом German VSITR
        
        Алгоритм German VSITR (7 проходів):
        1. Запис 0x00
        2. Запис 0xFF
        3-5. Запис псевдовипадкових даних (3 проходи)
        6. Запис 0xAA
        7. Запис псевдовипадкових даних
        """
        try:
            # Перевірка існування файлу
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Файл не знайдено: {filepath}")
            
            # Отримання розміру файлу
            file_size = os.path.getsize(filepath)
            logging.info(f"Початок безпечного видалення: {filepath} (розмір: {file_size} байт)")
            
            if status_callback:
                status_callback(f"Підготовка файлу до видалення...")
            
            # Зробити файл доступним для запису
            self.make_writable(filepath)
            
            # Виконання 7 проходів перезапису
            total_passes = len(self.passes)
            for pass_num, (pass_name, data_byte) in enumerate(self.passes, 1):
                if status_callback:
                    status_callback(f"Прохід {pass_num}/{total_passes}: {pass_name}")
                
                logging.info(f"Прохід {pass_num}: {pass_name}")
                
                def pass_progress(progress):
                    if progress_callback:
                        # Загальний прогрес = (завершені проходи + поточний прогрес) / загальна кількість проходів
                        total_progress = ((pass_num - 1) * 100 + progress) / total_passes
                        progress_callback(total_progress)
                
                success = self.overwrite_file(filepath, data_byte, file_size, pass_progress)
                if not success:
                    raise Exception(f"Помилка на проході {pass_num}")
            
            # Перейменування файлу
            if status_callback:
                status_callback("Перейменування файлу...")
            
            logging.info("Початок перейменування файлу")
            final_path = self.rename_file_randomly(filepath, times=3)
            
            # Остаточне видалення
            if status_callback:
                status_callback("Остаточне видалення...")
            
            os.remove(final_path)
            logging.info(f"Файл успішно видалено: {filepath}")
            
            if progress_callback:
                progress_callback(100)
            
            if status_callback:
                status_callback("Файл успішно видалено!")
            
            return True
            
        except Exception as e:
            error_msg = f"Помилка видалення файлу: {str(e)}"
            logging.error(error_msg)
            if status_callback:
                status_callback(f"ПОМИЛКА: {str(e)}")
            raise


class SecureFileDeleterGUI:
    """Графічний інтерфейс для програми безпечного видалення файлів"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Secure File Deleter - German VSITR")
        self.root.geometry("700x600")
        self.root.resizable(True, True)
        self.root.minsize(600, 500)
        
        self.deleter = SecureFileDeleter()
        self.selected_file = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Створення елементів інтерфейсу"""
        
        # Заголовок
        title_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        title_label = tk.Label(
            title_frame,
            text="Secure File Deleter",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            title_frame,
            text="German VSITR Algorithm (7-Pass Overwrite)",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Основна область
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Вибір файлу
        file_frame = tk.LabelFrame(main_frame, text="Вибір файлу", font=("Arial", 10, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.file_path_var = tk.StringVar()
        file_entry = tk.Entry(file_frame, textvariable=self.file_path_var, font=("Arial", 10), state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_frame,
            text="Вибрати файл",
            command=self.browse_file,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            padx=15
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Інформація про алгоритм
        info_frame = tk.LabelFrame(main_frame, text="Алгоритм German VSITR", font=("Arial", 10, "bold"), padx=10, pady=10)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = """Алгоритм виконує 7 проходів перезапису:
1. Запис байтів 0x00
2. Запис байтів 0xFF
3-5. Запис псевдовипадкових даних (3 проходи)
6. Запис байтів 0xAA
7. Запис псевдовипадкових даних

Після перезапису файл перейменовується 3 рази та видаляється."""
        
        info_label = tk.Label(info_frame, text=info_text, font=("Arial", 9), justify=tk.LEFT, fg="#34495e")
        info_label.pack(anchor=tk.W)
        
        # Прогрес
        progress_frame = tk.LabelFrame(main_frame, text="Прогрес", font=("Arial", 10, "bold"), padx=10, pady=10)
        progress_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.status_var = tk.StringVar(value="Очікування вибору файлу...")
        status_label = tk.Label(
            progress_frame,
            textvariable=self.status_var,
            font=("Arial", 9),
            fg="#7f8c8d"
        )
        status_label.pack(anchor=tk.W)
        
        # Кнопка видалення
        delete_btn = tk.Button(
            main_frame,
            text="БЕЗПЕЧНО ВИДАЛИТИ ФАЙЛ",
            command=self.delete_file,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 12, "bold"),
            cursor="hand2",
            padx=20,
            pady=10
        )
        delete_btn.pack(pady=10)
        
        # Попередження
        warning_label = tk.Label(
            main_frame,
            text="⚠️ УВАГА: Файл буде видалено НАЗАВЖДИ без можливості відновлення!",
            font=("Arial", 9, "bold"),
            fg="#e74c3c"
        )
        warning_label.pack(pady=(5, 0))
    
    def browse_file(self):
        """Вибір файлу через діалогове вікно"""
        filename = filedialog.askopenfilename(
            title="Виберіть файл для безпечного видалення",
            filetypes=[("Всі файли", "*.*")]
        )
        
        if filename:
            self.selected_file = filename
            self.file_path_var.set(filename)
            self.status_var.set(f"Вибрано файл: {os.path.basename(filename)}")
            logging.info(f"Вибрано файл: {filename}")
    
    def update_progress(self, value):
        """Оновлення прогрес-бару"""
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def update_status(self, message):
        """Оновлення статусу операції"""
        self.status_var.set(message)
        self.root.update_idletasks()
    
    def delete_file(self):
        """Видалення вибраного файлу"""
        if not self.selected_file:
            messagebox.showwarning("Попередження", "Будь ласка, виберіть файл для видалення!")
            return
        
        if not os.path.exists(self.selected_file):
            messagebox.showerror("Помилка", "Вибраний файл не існує!")
            self.selected_file = None
            self.file_path_var.set("")
            return
        
        # Підтвердження видалення
        file_name = os.path.basename(self.selected_file)
        file_size = os.path.getsize(self.selected_file)
        file_size_mb = file_size / (1024 * 1024)
        
        confirm = messagebox.askyesno(
            "Підтвердження видалення",
            f"Ви впевнені, що хочете НАЗАВЖДИ видалити файл?\n\n"
            f"Файл: {file_name}\n"
            f"Розмір: {file_size_mb:.2f} MB\n\n"
            f"Цю операцію НЕМОЖЛИВО скасувати!",
            icon='warning'
        )
        
        if not confirm:
            return
        
        # Скидання прогресу
        self.progress_var.set(0)
        self.update_status("Початок безпечного видалення...")
        
        try:
            # Виконання безпечного видалення
            self.deleter.secure_delete(
                self.selected_file,
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )
            
            messagebox.showinfo(
                "Успіх",
                f"Файл '{file_name}' успішно видалено!\n\n"
                f"Виконано 7 проходів перезапису за алгоритмом German VSITR."
            )
            
            # Скидання вибору
            self.selected_file = None
            self.file_path_var.set("")
            self.progress_var.set(0)
            self.update_status("Файл успішно видалено. Очікування нового файлу...")
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Не вдалося видалити файл:\n{str(e)}")
            self.progress_var.set(0)
            self.update_status(f"Помилка: {str(e)}")


def main():
    """Головна функція програми"""
    root = tk.Tk()
    app = SecureFileDeleterGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
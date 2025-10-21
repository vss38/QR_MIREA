import tkinter as tk
from tkinter import ttk
import uuid
import qrcode
from PIL import Image, ImageTk

# --- КОНСТАНТЫ ---
BASE_URL = "https://pulse.mirea.ru/lessons/visiting-logs/selfapprove?token="
WINDOW_TITLE = "Генератор QR-кодов"
QR_CODE_SIZE = 400  # Размер QR-кода в пикселях

class QRCodeApp:
    def __init__(self, master):
        self.master = master
        master.title(WINDOW_TITLE)
        master.resizable(False, False) # Запрещаем изменять размер окна

        # --- Создание виджетов ---
        
        # 1. Рамка для QR-кода и текста
        self.frame = ttk.Frame(master, padding="10")
        self.frame.pack()

        # 2. Место для изображения QR-кода (Label)
        self.qr_label = ttk.Label(self.frame)
        self.qr_label.pack(pady=10)

        # 3. Текстовая метка для отображения текущего токена
        self.token_label = ttk.Label(self.frame, text="Нажмите кнопку, чтобы начать", font=("Helvetica", 10))
        self.token_label.pack(pady=(0, 10))

        # 4. Кнопка для генерации нового кода
        self.generate_button = ttk.Button(self.frame, text="Сгенерировать новый QR-код", command=self.update_qr_code)
        self.generate_button.pack(pady=5)
        
        # --- Привязка клавиш ---
        # Обновление по нажатию на Enter или Пробел
        master.bind('<Return>', self.update_qr_code)
        master.bind('<space>', self.update_qr_code)

        # --- Первоначальный запуск ---
        self.update_qr_code()

    def update_qr_code(self, event=None):
        """
        Генерирует новый токен, создает QR-код и обновляет изображение в окне.
        """
        # 1. Генерируем новый уникальный токен
        new_token = str(uuid.uuid4())
        full_url = f"{BASE_URL}{new_token}"

        # 2. Обновляем текстовую метку с токеном
        self.token_label.config(text=f"Token: {new_token}")

        # 3. Создаем QR-код
        qr_img = qrcode.make(full_url)
        
        # 4. Конвертируем изображение для Tkinter
        #    Сначала изменим размер для красивого отображения
        resized_img = qr_img.resize((QR_CODE_SIZE, QR_CODE_SIZE), Image.Resampling.LANCZOS)
        
        #    Теперь конвертируем в формат, понятный Tkinter
        self.qr_image = ImageTk.PhotoImage(resized_img) # ВАЖНО: сохраняем ссылку в self!

        # 5. Обновляем изображение в окне
        self.qr_label.config(image=self.qr_image)


# --- Основная часть для запуска приложения ---
if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.mainloop()

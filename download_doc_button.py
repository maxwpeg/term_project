import tkinter as tk
from tkinter import filedialog

def load_file():
    file_path = filedialog.askopenfilename()
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, file_content)
    except FileNotFoundError:
        print("Файл не найден. Пожалуйста, убедитесь, что указали правильный путь к файлу.")
    except Exception as e:
        print("Произошла ошибка:", e)

# Создаем окно
root = tk.Tk()
root.title("Загрузка текстового файла")

# Создаем текстовое поле для отображения содержимого файла
text_area = tk.Text(root, wrap="word")
text_area.pack(expand=True, fill="both")

# Создаем кнопку для загрузки файла
load_button = tk.Button(root, text="Загрузить файл", command=load_file)
load_button.pack()

root.mainloop()

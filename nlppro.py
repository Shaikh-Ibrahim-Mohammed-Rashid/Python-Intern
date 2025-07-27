import tkinter as tk
from tkinter import ttk, messagebox
from gtts import gTTS
from googletrans import Translator
import os
import platform
import subprocess

translator = Translator()

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Arabic": "ar",
    "Chinese (Mandarin)": "zh-CN",
    "Japanese": "ja",
    "Russian": "ru"
}

def play_audio(file_path):
    system = platform.system()
    try:
        if system == "Windows":
            os.startfile(file_path)
        elif system == "Darwin":
            subprocess.run(["open", file_path])
        else:
            subprocess.run(["xdg-open", file_path])
    except Exception as e:
        messagebox.showerror("Playback Error", f"Could not play audio:\n{e}")

def convert_text_to_speech():
    text = text_input.get("1.0", tk.END).strip()
    lang_name = language_var.get()

    if not text:
        messagebox.showwarning("Input Error", "Please enter some text.")
        return

    lang_code = languages.get(lang_name, "en")

    try:
        if lang_code != "en":
            translated = translator.translate(text, dest=lang_code)
            translated_text = translated.text
        else:
            translated_text = text

        translated_output_var.set(translated_text)

        tts = gTTS(text=translated_text, lang=lang_code, slow=False)
        filename = "output.mp3"
        tts.save(filename)

        play_audio(filename)
        messagebox.showinfo("Success", f"Text translated to {lang_name} and spoken successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed:\n{e}")

root = tk.Tk()
root.title("BE-B B2 Batch Text to Speech with Translation")
root.geometry("550x500")
root.resizable(False, False)

ttk.Label(root, text="BE-B B2 Batch NLP Project !", font=("Helvetica", 18)).pack(pady=10)

ttk.Label(root, text="Enter Text:").pack(anchor="w", padx=20)
text_input = tk.Text(root, height=5, width=60, wrap=tk.WORD)
text_input.pack(padx=20, pady=5)

ttk.Label(root, text="Select Language:").pack(anchor="w", padx=20, pady=(10, 0))
language_var = tk.StringVar()
language_menu = ttk.Combobox(root, textvariable=language_var, values=list(languages.keys()), state="readonly", width=30)
language_menu.current(0)
language_menu.pack(padx=20, pady=5)

ttk.Label(root, text="Translated Text:").pack(anchor="w", padx=20, pady=(10, 0))
translated_output_var = tk.StringVar()
translated_output_label = ttk.Label(root, textvariable=translated_output_var, wraplength=500, foreground="blue")
translated_output_label.pack(padx=20, pady=5)

ttk.Button(root, text="Translate and Play", command=convert_text_to_speech).pack(pady=20)

root.mainloop()

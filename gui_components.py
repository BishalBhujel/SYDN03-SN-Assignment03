# this file will have the GUI interface functions
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from models import ImageToText, TextToImage

class AIApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Tkinter GUI")
        self.geometry("800x600")

        # Models
        self.image_to_text = ImageToText()
        self.text_to_image = TextToImage()

        # Widgets
        self.create_widgets()

        def create_widgets(self):
        # Input selection
        self.label = tk.Label(self, text="Choose Task:", font=("Arial", 14))
        self.label.pack(pady=10)

        self.task_var = tk.StringVar(value="Image→Text")
        self.dropdown = tk.OptionMenu(self, self.task_var, "Image→Text", "Text→Image")
        self.dropdown.pack(pady=5)

        # Input field
        self.input_text = tk.Entry(self, width=50)
        self.input_text.pack(pady=10)

        self.browse_btn = tk.Button(self, text="Browse File", command=self.browse_file)
        self.browse_btn.pack()

        # Run button
        self.run_btn = tk.Button(self, text="Run", command=self.run_task)
        self.run_btn.pack(pady=20)

        # Output display
        self.output_label = tk.Label(self, text="Output will appear here", wraplength=700)
        self.output_label.pack(pady=10)

        self.image_label = tk.Label(self)
        self.image_label.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.input_text.delete(0, tk.END)
        self.input_text.insert(0, file_path)
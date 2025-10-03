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
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch
import os


# Defining a base class showing the example of encapsulation
class AIModel:
    def __init__(self, name, category, description):
        # Showing the encapsulation example by using the encapsulated attributes like name, category and description
        self._name = name
        self._category = category
        self._description = description

    # defining a get_info base function
    def get_info(self):
        return f"Model: {self._name}\nCategory: {self._category}\n{self._description}"

    # defining a run base function
    def run(self, input_data):
        raise NotImplementedError("Subclasses must implement run()")


# importing models Image-to-Text Model 
# This function shows the example of Inheritance by inheriting the properties from AIModel class and Polymorphism
class ImageToText(AIModel):
    def __init__(self):
        super().__init__(
            "nlpconnect/vit-gpt2-image-captioning",
            "Vision → Image-to-Text",
            "Generates captions for input images."
        )
        self.model = pipeline("image-to-text", model="nlpconnect/vit-gpt2-image-captioning")

    def run(self, image_path):
        result = self.model(image_path)
        return result[0]['generated_text']

# importing models Text-to-Image Model
# This function shows the example of Inheritance and Overriding
class TextToImage(AIModel):
    def __init__(self):
        super().__init__(
            "runwayml/stable-diffusion-v1-5",
            "Vision → Text-to-Image",
            "Generates images from text prompts using Stable Diffusion."
        )
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if device == "cuda":
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16
            ).to("cuda")
        else:
            self.pipe = StableDiffusionPipeline.from_pretrained(
                "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float32
            ).to("cpu")

        self.device = device

    def run(self, prompt):
        image = self.pipe(prompt).images[0]
        os.makedirs("assets", exist_ok=True)
        out_path = "assets/generated.png"
        image.save(out_path)
        return f"Image saved at {out_path} (running on {self.device})"
    
class Logger:
    # Defining a decorators called staticmethod
    @staticmethod
    # Creating a log function for logging every steps taking place in the process
    def log_action(func):
        def wrapper(*args, **kwargs):
            # Prints the function name that is being called
            print(f"Running: {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    
# Making a GUIApp which uses multiple inheitance from class Tk and Logger
class GUIApp(tk.Tk, Logger): 
    def __init__(self):
        super().__init__()
        self.title("Tkinter AI GUI")
        self.geometry("800x600")

        self.model = None
        self.create_widgets()

    # Define a function to create a menubar
    def create_widgets(self):
        # Define a menu Bar
        menubar = tk.Menu(self)
        self.config(menu=menubar)
        menubar.add_command(label="Models")
        menubar.add_command(label="Help")

        # Define a model selection module
        frame_top = tk.Frame(self)
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="Model Selection:").grid(row=0, column=0, padx=5)
        self.model_var = tk.StringVar()
        model_dropdown = ttk.Combobox(frame_top, textvariable=self.model_var, values=["Image-to-Text", "Text-to-Image"])
        model_dropdown.grid(row=0, column=1, padx=5)

        load_btn = tk.Button(frame_top, text="Load Model", command=self.load_model)
        load_btn.grid(row=0, column=2, padx=5)

        # Define a text bar which takes the user input 
        input_frame = tk.LabelFrame(self, text="User Input Section")
        input_frame.pack(fill="x", padx=10, pady=5)

        self.input_type = tk.StringVar(value="Text")
        tk.Radiobutton(input_frame, text="Text", variable=self.input_type, value="Text").grid(row=0, column=0, padx=5)
        tk.Radiobutton(input_frame, text="Image", variable=self.input_type, value="Image").grid(row=0, column=1, padx=5)

        browse_btn = tk.Button(input_frame, text="Browse", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5)

        self.input_text = tk.Text(input_frame, height=5, width=60)
        self.input_text.grid(row=1, column=0, columnspan=3, pady=5)

        # Define a section which shows the output
        output_frame = tk.LabelFrame(self, text="Model Output Section")
        output_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(output_frame, text="Output Display:").pack(anchor="w")
        self.output_text = tk.Text(output_frame, height=8, width=80)
        self.output_text.pack()

        # Create a button for Run Model
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=5)

        run1_btn = tk.Button(btn_frame, text="Run Model", command=self.run_model)
        run1_btn.grid(row=0, column=0, padx=5)

        clear_btn = tk.Button(btn_frame, text="Clear", command=self.clear_text)
        clear_btn.grid(row=0, column=1, padx=5)

        # Create a section which contains the model information and explanation for OOP concepts used
        info_frame = tk.LabelFrame(self, text="Model Information & Explanation")
        info_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.model_info = tk.Text(info_frame, height=6, width=40)
        self.model_info.grid(row=0, column=0, padx=5, pady=5)

        self.oop_info = tk.Text(info_frame, height=6, width=40)
        self.oop_info.grid(row=0, column=1, padx=5, pady=5)

    # Define a function which allows to browse through the files in a desktop
    def browse_file(self):
        # Define a try catch block while browsing through the files
        try:
            # Use the safer Cocoa call style on macOS
            filetypes = [
                ("Image files", "*.png *.jpg *.jpeg *.bmp *.gif"),
                ("All files", "*.*")
            ]

            file_path = filedialog.askopenfilename(
                parent=self,
                title="Choose an image",
                initialdir=os.path.expanduser("~"),
                filetypes=filetypes
            )

            if file_path:
                self.input_text.delete("1.0", tk.END)
                self.input_text.insert(tk.END, file_path)

        # Catching the exception that might cause while browsing the files
        except Exception as e:
            import traceback
            # Showing the error message incase the file browsing failed
            messagebox.showerror("Error", f"Browse failed:\n{e}\n\n{traceback.format_exc()}")

    # Defining a function to load the models used in the assignments for furthur processing
    def load_model(self):
        model_choice = self.model_var.get()
        if model_choice == "Image-to-Text":
            self.model = ImageToText()
        elif model_choice == "Text-to-Image":
            self.model = TextToImage()
        else:
            messagebox.showerror("Error", "Select a model first!")
            return

        # Updating model info
        self.model_info.delete("1.0", tk.END)
        self.model_info.insert(tk.END, self.model.get_info())

        # Explanation of OOP concepts used
        explanation = (
            "- Multiple Inheritance: GUIApp inherits from Tk and Logger\n"
            "- Encapsulation: Private attributes in AIModel (_name, _category)\n"
            "- Polymorphism: run() behaves differently for each model\n"
            "- Method Overriding: TextToImage and ImageToText override run()\n"
            "- Decorators: Logger.log_action for function tracking\n"
        )
        self.oop_info.delete("1.0", tk.END)
        self.oop_info.insert(tk.END, explanation)

        messagebox.showinfo("Model Loaded", f"{model_choice} model is ready!")

    @Logger.log_action
    def run_model(self):
        if not self.model:
            messagebox.showerror("Error", "Please load a model first!")
            return

        input_data = self.input_text.get("1.0", tk.END).strip()
        if not input_data:
            messagebox.showerror("Error", "Please enter text or select an image.")
            return

        try:
            output = self.model.run(input_data)
            self.output_text.insert(tk.END, f"\n{output}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.delete("1.0", tk.END)


# ------------------------------
# Run the App
# ------------------------------
if __name__ == "__main__":
    app = GUIApp()
    app.mainloop()
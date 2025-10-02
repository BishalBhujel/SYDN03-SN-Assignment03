import tkinter as tk
from tkinter import filedialog, messagebox
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
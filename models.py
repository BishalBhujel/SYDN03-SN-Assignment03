from transformers import pipeline
from diffusers import StableDiffusionPipeline
import torch

class ImageToText:
    """Image Captioning Model"""
    def __init__(self, repo_id="nlpconnect/vit-gpt2-image-captioning"):
        self.model = pipeline("image-to-text", model=repo_id)

    def generate_caption(self, image_path):
        result = self.model(image_path)
        return result[0]['generated_text']


class TextToImage:
    """Text-to-Image Model using Stable Diffusion"""
    def __init__(self, repo_id="runwayml/stable-diffusion-v1-5"):
        # Detect device
        device = "cuda" if torch.cuda.is_available() else "cpu"

        if device == "cuda":
            # GPU → use float16 (faster, memory efficient)
            self.pipe = StableDiffusionPipeline.from_pretrained(
                repo_id, torch_dtype=torch.float16
            ).to("cuda")
        else:
            # CPU → must use float32
            self.pipe = StableDiffusionPipeline.from_pretrained(
                repo_id, torch_dtype=torch.float32
            ).to("cpu")

    def generate_image(self, prompt, output_path="output.png"):
        image = self.pipe(prompt).images[0]
        image.save(output_path)
        return output_path

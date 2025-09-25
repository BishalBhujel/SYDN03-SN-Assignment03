from transformers import pipeline

gen = pipeline("text-generation", model="distilgpt2")
out = gen("Write a concise summary about machine learning:", max_length=60, num_return_sequences=1)
print(out[0]['generated_text'])

clf = pipeline("image-classification", model="microsoft/resnet-50")
res = clf("canva.webp", top_k=3)
print(res)
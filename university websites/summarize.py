"""
import re
from transformers import LEDForConditionalGeneration, LEDTokenizer
import torch

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    text = re.sub(r'<[^>]+>', '', text)  # Remove HTML tags if present
    return text

def summarize_text(long_text, max_length_, min_length_):
    model = LEDForConditionalGeneration.from_pretrained('allenai/led-base-16384')
    tokenizer = LEDTokenizer.from_pretrained('allenai/led-base-16384')

    cleaned_text = clean_text(long_text)

    inputs = tokenizer(
        cleaned_text,
        return_tensors="pt",
        max_length=16384,
        truncation=True)
    
    # Set global attention on the first token
    global_attention_mask = torch.zeros_like(inputs['input_ids'])
    global_attention_mask[:, 0] = 1

    if len(cleaned_text) > max_length_:
        summary_ids = model.generate(
            inputs['input_ids'],
            global_attention_mask=global_attention_mask,
            max_length=400,  # Adjust summary length
            num_beams=5,     # Experiment with beam search settings
            early_stopping=True
        )
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        return summary
    else:
        return cleaned_text
"""

from transformers import pipeline

def summarize_text(long_text, max_length_, min_length_):

    summarizer = pipeline(
        task="summarization",
        model="sshleifer/distilbart-cnn-12-6",
        revision="main"
    )

    if len(long_text) > max_length_ and len(long_text) < 1024:
        summary = summarizer(long_text, max_length=max_length_, min_length=min_length_, do_sample=False)
        return summary[0]['summary_text']
    else:
        return long_text
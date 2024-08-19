import torch
from transformers import pipeline, AutoTokenizer

def get_basic_summary(formatted_rows, column_name, model_max_length=2048):
    print(formatted_rows)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")

    text_string = ", ".join([formatted_rows[i][column_name] for i in range(len(formatted_rows))])
    input_ids = tokenizer(text_string, return_tensors="pt")["input_ids"]

    max_length = min(input_ids.shape[1], model_max_length)

    return summarizer(text_string, max_length=max_length-1, min_length=max_length//10, do_sample=False)[0]['summary_text']
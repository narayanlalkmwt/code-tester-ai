import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

# Initialize tokenizer and model
tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base", num_labels=2)

def preprocess_multilang_data(data, tokenizer, max_len=128):
    inputs = []
    for item in data:
        question = item["question"]
        incorrect_code = item["incorrect_code"]
        language = item["language"]

        # Format input with language
        input_text = f"[{language}] {question} Code:\n{incorrect_code}"
        tokenized_input = tokenizer(
            input_text, max_length=max_len, truncation=True, padding="max_length", return_tensors="pt"
        )
        
        label = torch.tensor(item["label"], dtype=torch.long)
        inputs.append({
            "input_ids": tokenized_input["input_ids"].squeeze(),
            "attention_mask": tokenized_input["attention_mask"].squeeze(),
            "label": label
        })
    return inputs

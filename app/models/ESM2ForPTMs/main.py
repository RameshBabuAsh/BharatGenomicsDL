from transformers import AutoModelForTokenClassification, AutoTokenizer
from peft import PeftModel
import torch
import gc


def ESM2ForPTMs(proteinSequence):
    model_path = "AmelieSchreiber/esm2_t30_150M_ptm_qlora_2100K_1000"
    base_model_path = "facebook/esm2_t30_150M_UR50D"

    # Load the model
    base_model = AutoModelForTokenClassification.from_pretrained(base_model_path)
    loaded_model = PeftModel.from_pretrained(base_model, model_path)

    # Ensure the model is in evaluation mode
    loaded_model.eval()

    # Load the tokenizer
    loaded_tokenizer = AutoTokenizer.from_pretrained(base_model_path)

    # Protein sequence for inference
    protein_sequence = proteinSequence  # Replace with your actual sequence

    # Tokenize the sequence
    inputs = loaded_tokenizer(protein_sequence, return_tensors="pt", truncation=True, max_length=1024, padding='max_length')

    # Run the model
    with torch.no_grad():
        logits = loaded_model(**inputs).logits

    # Get predictions
    tokens = loaded_tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])  # Convert input ids back to tokens
    predictions = torch.argmax(logits, dim=2)

    # Define labels
    # id2label = {
    #     0: "No ptm site",
    #     1: "ptm site"
    # }

    result = []

    for token, prediction in zip(tokens, predictions[0].numpy()):
        if token not in ['<pad>', '<cls>', '<eos>']:
            result.append((token, prediction))

    # Free the memory
    del base_model
    del loaded_model
    del loaded_tokenizer
    del inputs
    del logits
    del tokens
    del predictions
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    return result

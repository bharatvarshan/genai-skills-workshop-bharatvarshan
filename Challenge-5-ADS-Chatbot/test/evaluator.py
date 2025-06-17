import pandas as pd
import re
from evaluate import load
from sentence_transformers import SentenceTransformer, util

# Load Hugging Face metrics
rouge = load("rouge")
bertscore = load("bertscore")

# Load sentence transformer for semantic similarity
embed_model = SentenceTransformer("all-MiniLM-L6-v2")

# Basic sentence split
def simple_sentence_split(text):
    return re.split(r'[.!?]+', text.strip())

# Basic word split
def simple_word_tokenize(text):
    return re.findall(r'\b\w+\b', text.lower())

# Heuristic: average sentence length = proxy for fluency
def compute_fluency(text):
    sentences = simple_sentence_split(text)
    words = simple_word_tokenize(text)
    avg_sentence_len = len(words) / max(len(sentences), 1)

    if avg_sentence_len > 20:
        return 2.5
    elif avg_sentence_len > 12:
        return 4.0
    else:
        return 5.0

# Semantic similarity using sentence embeddings
def compute_groundedness(reference, prediction):
    ref_embedding = embed_model.encode(reference, convert_to_tensor=True)
    pred_embedding = embed_model.encode(prediction, convert_to_tensor=True)
    cosine_sim = util.pytorch_cos_sim(ref_embedding, pred_embedding).item()
    return round(cosine_sim * 5, 2)  # scale 0–5

# Main evaluation
def evaluate_text(reference, prediction):
    """
    This function evalues the output using Google Evaluation API
    """
    rouge_result = rouge.compute(predictions=[prediction], references=[reference])
    bert_result = bertscore.compute(predictions=[prediction], references=[reference], lang="en")

    fluency = compute_fluency(prediction)
    groundedness = compute_groundedness(reference, prediction)

    return pd.DataFrame([{
        "reference": reference,
        "prediction": prediction,
        "rouge1": rouge_result["rouge1"],
        "rouge2": rouge_result["rouge2"],
        "rougeL": rouge_result["rougeL"],
        "rougeLsum": rouge_result.get("rougeLsum", 0),
        "bleu": 0.0,
        "bertscore_precision": bert_result["precision"][0],
        "bertscore_recall": bert_result["recall"][0],
        "bertscore_f1": bert_result["f1"][0],
        "fluency_score": fluency,
        "groundedness_score": groundedness
    }])

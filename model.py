"""
model.py — BART summarization model loader.
Tries the fine-tuned local model first; falls back to facebook/bart-large-cnn.
If transformers is not installed or model loading fails, uses extractive fallback.
"""

import os
import re

# ── Try loading transformers ───────────────────────────────────────────────────
try:
    from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, pipeline as hf_pipeline
    import torch
    _HF_AVAILABLE = True
except ImportError:
    _HF_AVAILABLE = False

# ── Model state ───────────────────────────────────────────────────────────────
_bart_pipeline = None
_ft_model      = None
_ft_tokenizer  = None
_device        = "cpu"
_MODELS_READY  = False


def _init_models():
    global _bart_pipeline, _ft_model, _ft_tokenizer, _device, _MODELS_READY
    if _MODELS_READY:
        return
    if not _HF_AVAILABLE:
        _MODELS_READY = True
        return

    try:
        _device = "cuda" if torch.cuda.is_available() else "cpu"
        print("[model.py] Loading facebook/bart-large-cnn ...")
        _bart_pipeline = hf_pipeline(
            "summarization",
            model="facebook/bart-large-cnn",
            device=0 if _device == "cuda" else -1
        )
        print("[model.py] bart-large-cnn ready")
    except Exception as e:
        print(f"[model.py] WARNING bart-large-cnn failed: {e}")
        _bart_pipeline = None

    BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
    MODEL_PATH = os.path.join(BASE_DIR, "..", "bart_xsum_model", "content", "bart_xsum_model")

    if os.path.isdir(MODEL_PATH):
        try:
            print(f"[model.py] Loading fine-tuned model ...")
            _ft_tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large-cnn")
            _ft_model     = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(_device)
            print("[model.py] Fine-tuned model ready")
        except Exception as e:
            print(f"[model.py] Fine-tuned model failed: {e}")
            _ft_model = None
    else:
        print(f"[model.py] Fine-tuned model path not found, using base BART only.")

    _MODELS_READY = True


def smart_summary(text: str, max_length: int = 200, min_length: int = 40) -> str:
    _init_models()
    words = text.split()
    if len(words) > 600:
        text = " ".join(words[:600])

    bart_out = _run_bart(text, max_length, min_length)
    ft_out   = _run_finetuned(text, max_length)

    if bart_out and ft_out:
        return bart_out if _score(bart_out) >= _score(ft_out) else ft_out
    if bart_out:
        return bart_out
    if ft_out:
        return ft_out
    return _extractive_fallback(text)


def _run_bart(text, max_length, min_length):
    if _bart_pipeline is None:
        return ""
    try:
        result = _bart_pipeline(text, max_length=max_length, min_length=min_length, do_sample=False, truncation=True)
        return result[0]["summary_text"].strip()
    except Exception as e:
        print(f"[model.py] BART error: {e}")
        return ""


def _run_finetuned(text, max_length):
    if _ft_model is None or _ft_tokenizer is None:
        return ""
    try:
        inputs = _ft_tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        inputs = {k: v.to(_device) for k, v in inputs.items()}
        with torch.no_grad():
            outputs = _ft_model.generate(**inputs, max_new_tokens=max_length, num_beams=4, no_repeat_ngram_size=3, length_penalty=2.0)
        return _ft_tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    except Exception as e:
        print(f"[model.py] Fine-tuned error: {e}")
        return ""


def _score(text):
    tokens = text.split()
    return len(tokens) + len(set(tokens))


def _extractive_fallback(text):
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return " ".join(sentences[:3]) if sentences else text[:300]

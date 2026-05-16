"""
pipeline.py — Orchestrates the AI extraction pipeline.
Uses model.py (BART) for summarization, action items, and decisions.
"""

from model import smart_summary
from prompts import summary_prompt, action_items_prompt, decision_prompt

# Holds last transcript so chatbot can reference it
last_context = ""


def process_text(text: str):
    global last_context

    text = text.strip()
    if not text:
        return "No input provided.", "No action items found.", "No decisions found."

    last_context = text

    summary   = smart_summary(summary_prompt(text),   max_length=180, min_length=60)
    actions   = smart_summary(action_items_prompt(text), max_length=200, min_length=30)
    decisions = smart_summary(decision_prompt(text),  max_length=200, min_length=30)

    return summary, actions, decisions

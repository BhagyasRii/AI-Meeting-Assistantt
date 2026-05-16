"""
prompts.py — Prompt templates for summary, action items, and decisions.
"""


def summary_prompt(text: str) -> str:
    return f"""
You are an AI meeting assistant.

Generate a detailed and well-structured summary of the meeting.

Requirements:
- Write in 80–120 words
- Cover all key discussion points
- Include important outcomes and conclusions
- Maintain clarity and professional tone
- Do NOT add unrelated information

Meeting Transcript:
{text}
"""


def action_items_prompt(text: str) -> str:
    return f"""
You are an AI assistant extracting action items from a meeting.

Identify ALL action items clearly.

Strict Format (follow exactly):

Task:
Owner:
Deadline:

Task:
Owner:
Deadline:

Rules:
- Extract multiple tasks if present
- If owner is not mentioned → write "Not specified"
- If deadline is not mentioned → write "Not specified"
- Do NOT skip fields

Meeting Transcript:
{text}
"""


def decision_prompt(text: str) -> str:
    return f"""
You are an AI assistant identifying decisions made in a meeting.

Extract all decisions clearly.

Strict Format (follow exactly):

Decision:
Responsible:
Impact:

Decision:
Responsible:
Impact:

Rules:
- If responsible person is not mentioned → write "Not specified"
- If impact is not clear → infer briefly
- Do NOT leave any field empty

Meeting Transcript:
{text}
"""

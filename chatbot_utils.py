"""
chatbot_utils.py — Q&A over meeting transcript using BART.
Builds a focused prompt and runs it through smart_summary.
"""

from model import smart_summary


def ask_question(context: str, question: str) -> str:
    if not context or not context.strip():
        return "No meeting data available. Please analyse a transcript first."

    if not question or not question.strip():
        return "Please enter a question."

    # Build a focused, extractive-friendly prompt
    # BART works best when the answer is likely in the first part of the text,
    # so we place the question as a "headline" hint at the top.
    prompt = (
        f"Question: {question}\n\n"
        f"Answer based only on the following meeting transcript:\n\n"
        f"{context}"
    )

    answer = smart_summary(prompt, max_length=150, min_length=20)

    if not answer or len(answer.strip()) < 5:
        return "I could not find a clear answer in the meeting transcript."

    return answer

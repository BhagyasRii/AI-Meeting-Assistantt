import gradio as gr
from pipeline import process_text, last_context
from email_utils import send_email
from pdf_utils import generate_pdf
from chatbot_utils import ask_question


def launch_app():
    with gr.Blocks() as app:

        gr.Markdown("# AI Meeting Intelligence System")

        # INPUT
        text_input = gr.Textbox(
            label="Enter Meeting Transcript",
            lines=10
        )

        btn = gr.Button("Analyze")

        # OUTPUTS
        summary = gr.Textbox(label="Summary", lines=6)
        actions = gr.Textbox(label="Action Items", lines=6)
        decisions = gr.Textbox(label="Decisions", lines=6)

        btn.click(
            process_text,
            inputs=[text_input],
            outputs=[summary, actions, decisions]
        )

        # ================= EMAIL =================
        gr.Markdown("## 📧 Send Email")

        email_input = gr.Textbox(label="Receiver Email")
        send_btn = gr.Button("Send Email")
        email_status = gr.Textbox(label="Status")

        send_btn.click(
            send_email,
            inputs=[email_input, summary, actions, decisions],
            outputs=[email_status]
        )

        # ================= PDF =================
        gr.Markdown("## 📄 Download Report")

        pdf_btn = gr.Button("Generate PDF")
        pdf_file = gr.File(label="Download PDF")

        pdf_btn.click(
            generate_pdf,
            inputs=[summary, actions, decisions],
            outputs=[pdf_file]
        )

        # ================= CHATBOT =================
        gr.Markdown("## 🤖 Ask Questions")

        question = gr.Textbox(label="Ask a question")
        answer = gr.Textbox(label="Answer", lines=5)

        ask_btn = gr.Button("Ask")

        ask_btn.click(
            lambda q: ask_question(last_context, q),
            inputs=[question],
            outputs=[answer]
        )

    app.launch(debug=True)

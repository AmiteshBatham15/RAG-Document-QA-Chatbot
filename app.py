
import gradio as gr
from rag_pipeline import build_vector_store, answer_question

vector_store = None

def process_pdfs(files):
    global vector_store
    if not files:
        return "Please upload at least one PDF."
    pdf_paths = [file.name for file in files]
    try:
        vector_store = build_vector_store(pdf_paths)
        return f"Successfully processed {len(pdf_paths)} PDF file(s)."
    except Exception as error:
        return f"Error processing PDFs: {error}"



def chat(message, history):
    if vector_store is None:
        return "Please upload and process your PDFs first."

    try:
        answer, sources = answer_question(message, vector_store)

        # Ensure the answer is a string.
        if isinstance(answer, list):
            answer = "\n".join(
                item.get("text", str(item))
                if isinstance(item, dict)
                else str(item)
                for item in answer
            )
        elif not isinstance(answer, str):
            answer = str(answer)

        answer = answer.strip()

        # Do not display sources for the fallback response.
        fallback_phrases = [
            "i could not find it in the uploaded documents",
            "i could not find the answer in the uploaded documents",
            "i could not find the answer in the provided context",
        ]

        if any(phrase in answer.lower() for phrase in fallback_phrases):
            return answer

        # Format unique source references only.
        source_lines = []
        seen_sources = set()

        for source in sources or []:
            filename = source.get("source", "Unknown")
            page = source.get("page", "Unknown")

            source_key = (filename, page)

            if source_key not in seen_sources:
                seen_sources.add(source_key)
                source_lines.append(f"- {filename}, page {page}")

        if source_lines:
            source_text = "\n\nSources:\n" + "\n".join(source_lines)
            return answer + source_text

        return answer

    except Exception as error:
        import traceback
        traceback.print_exc()
        return f"Error answering question: {error}"



with gr.Blocks(title="RAG Document Q&A Chatbot") as demo:
    gr.Markdown("# RAG Document Q&A Chatbot")
    gr.Markdown("Upload PDFs and ask questions about their contents.")
    pdf_upload = gr.File(
        label="Upload PDF documents",
        file_count="multiple",
        file_types=[".pdf"],
        type="filepath",
    )
    process_button = gr.Button("Process PDFs")
    status = gr.Textbox(label="Processing status", interactive=False)
    process_button.click(fn=process_pdfs, inputs=pdf_upload, outputs=status)
    chatbot = gr.ChatInterface(fn=chat, title="Ask your documents")

if __name__ == "__main__":
    demo.launch()
    
    



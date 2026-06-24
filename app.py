!pip install gradio pymupdf google-generativeai

import gradio as gr
import fitz
import google.generativeai as genai

genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

def extract_text_from_pdf(pdf_file):
    doc = fitz.open(pdf_file)
    text = ""
    for page in doc:
        text += page.get_text()
        if len(text) > 12000:
            break
    return text[:12000]

def analyze_resume(text):
    prompt = f"""
You are an ATS resume checker.

Return:

- ATS Score /100
- Strengths (max 3)
- Weaknesses (max 3)
- Missing Skills (max 5)
- Improvements (max 5)

Resume:
{text}
"""
    return model.generate_content(prompt).text

def process_resume(pdf_file):
    if pdf_file is None:
        return "⚠️ Upload a PDF first."
    text = extract_text_from_pdf(pdf_file.name)
    if not text.strip():
        return "❌ No readable text found."
    return analyze_resume(text)

css = """
body {
    margin: 0;
    background: radial-gradient(circle at top, #0b1220, #070b14);
    color: white;
    font-family: Arial, sans-serif;
}

.gradio-container {
    max-width: 100% !important;
    padding: 20px !important;
}

.header-box {
    text-align: center;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 16px;
    background: linear-gradient(135deg, #0f1b33, #0b1220);
    border: 1px solid #2b2b55;
    box-shadow: 0 8px 20px rgba(0,0,0,0.4);
}

.header-box h1 {
    margin: 0;
    font-size: 28px;
    background: linear-gradient(to right, #a855f7, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.main-grid {
    display: grid;
    grid-template-columns: 1fr 1.5fr 1fr;
    gap: 18px;
    height: 78vh;
}

.panel {
    background: linear-gradient(145deg, #0f1a2e, #0b1220);
    border: 1px solid #1f2a44;
    border-radius: 18px;
    padding: 18px;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    box-shadow: 0 10px 25px rgba(0,0,0,0.35);
    overflow: hidden;
}

.panel h2 {
    margin-bottom: 10px;
}

.panel p, .panel li {
    opacity: 0.85;
    line-height: 1.5;
}

input, .gradio-file {
    border-radius: 10px !important;
}

button {
    width: 100% !important;
    margin-top: 15px;
    background: linear-gradient(to right, #a855f7, #6366f1) !important;
    color: white !important;
    font-weight: bold !important;
    border-radius: 12px !important;
    border: none !important;
    padding: 10px;
}

textarea {
    background: #0b1220 !important;
    color: #ffffff !important;
}
"""

with gr.Blocks(css=css, theme=gr.themes.Soft()) as app:
    gr.HTML("""
    <div class="header-box">
        <h1>🚀 AI Resume ATS Dashboard</h1>
    </div>
    """)

    with gr.Row(elem_classes="main-grid"):

        with gr.Column(elem_classes="panel"):
            gr.Markdown("## ⚙️ Controls")
            gr.Markdown("""
How it works
1. Upload your resume
2. AI analyzes ATS score
3. Get instant improvements
4. Optimize for hiring
""")

        with gr.Column(elem_classes="panel"):
            gr.Markdown("## 📄 Upload Resume Area")
            file_input = gr.File(label="Drop your PDF here")

            gr.Markdown("""
What AI checks:
- Formatting
- Keywords
- Skills match
- ATS compatibility
""")

            btn = gr.Button("🚀 Analyze Resume")

        with gr.Column(elem_classes="panel"):
            gr.Markdown("## 📊 AI Report Output")

            output = gr.Textbox(label="Result", lines=20)

    btn.click(
        fn=process_resume,
        inputs=file_input,
        outputs=output
    )

app.queue()
app.launch()

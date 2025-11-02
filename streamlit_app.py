import streamlit as st
from openai import OpenAI
import pdfplumber

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload documents below and ask a question about them – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # 複数ファイル対応
    uploaded_files = st.file_uploader(
        "Upload documents (.txt, .md, .pdf)", type=("txt", "md", "pdf"), accept_multiple_files=True
    )

    question = st.text_area(
        "Now ask a question about the documents!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_files,
    )

    if uploaded_files and question:
        documents = []
        for uploaded_file in uploaded_files:
            if uploaded_file.type == "application/pdf":
                with pdfplumber.open(uploaded_file) as pdf:
                    text = ""
                    for page in pdf.pages:
                        text += page.extract_text() or ""
                documents.append(text)
            else:
                documents.append(uploaded_file.read().decode())

        # 各ドキュメントを区切ってまとめる
        all_documents = "\n\n---\n\n".join(documents)
        messages = [
            {
                "role": "user",
                "content": f"Here are the documents:\n{all_documents}\n\n---\n\n{question}",
            }
        ]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)

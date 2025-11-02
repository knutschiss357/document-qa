import streamlit as st
from openai import OpenAI
import pdfplumber  # 追加

# Show title and description.
st.title("📄 Document question answering")
st.write(
    "Upload a document below and ask a question about it – GPT will answer! "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

openai_api_key = st.text_input("OpenAI API Key", type="password")
if not openai_api_key:
    st.info("Please add your OpenAI API key to continue.", icon="🗝️")
else:
    client = OpenAI(api_key=openai_api_key)

    # PDF対応
    uploaded_file = st.file_uploader(
        "Upload a document (.txt, .md, .pdf)", type=("txt", "md", "pdf")
    )

    question = st.text_area(
        "Now ask a question about the document!",
        placeholder="Can you give me a short summary?",
        disabled=not uploaded_file,
    )

    if uploaded_file and question:
        # ファイルタイプ判定
        if uploaded_file.type == "application/pdf":
            # PDFテキスト抽出
            with pdfplumber.open(uploaded_file) as pdf:
                document = ""
                for page in pdf.pages:
                    document += page.extract_text() or ""
        else:
            document = uploaded_file.read().decode()

        messages = [
            {
                "role": "user",
                "content": f"Here's a document: {document} \n\n---\n\n {question}",
            }
        ]

        stream = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            stream=True,
        )

        st.write_stream(stream)

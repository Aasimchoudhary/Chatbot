# Book 1 Locked Chatbot

A simple Streamlit RAG chatbot locked to Book 1 only.

## What this version does
- Users can only ask questions.
- Users cannot upload PDFs, files, or photos.
- The app reads a preloaded Book 1 PDF from the server.

## Preparation
1. Install Python 3.10 or newer.
2. Create an OpenAI API key.
3. Put the key in an environment variable named `OPENAI_API_KEY`.
4. Put your Book 1 PDF in the project folder and name it `book1.pdf`, or set `BOOK1_PATH`.
5. Install requirements.
6. Run the Streamlit app.

## Commands
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Best site to deploy
- Streamlit Community Cloud for easiest deployment
- Render for simple Python hosting

## Notes
- This version uses only Book 1.
- Book 1 appears scan-heavy and may need OCR for better results.
- This app preserves the original PDF; it does not remove images from the source file.

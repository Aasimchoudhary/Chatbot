import os
import streamlit as st
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

st.set_page_config(page_title='Book 1 Chatbot', page_icon='📘', layout='wide')
st.title('📘 Book 1 AI Chatbot')
st.caption('Ask questions from the book only.')

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
BOOK1_PATH = os.getenv('BOOK1_PATH', 'book1.pdf')

if not OPENAI_API_KEY:
    st.error('Set OPENAI_API_KEY before running the app.')
    st.stop()

if not os.path.exists(BOOK1_PATH):
    st.error('Book 1 PDF not found. Place the PDF next to app.py or set BOOK1_PATH.')
    st.stop()

@st.cache_resource
def build_chain(pdf_path: str):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    for d in docs:
        d.metadata['book_name'] = os.path.basename(pdf_path)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1200, chunk_overlap=200)
    chunks = splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings(model='text-embedding-3-large')
    vectorstore = FAISS.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={'k': 5})
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True,
        chain_type='stuff'
    )

with st.sidebar:
    st.header('Book access')
    st.write('This chatbot is locked to Book 1 only.')
    st.write('Users cannot upload files or images.')
    st.write('Original source PDF remains unchanged.')
    st.write('If the PDF is scan-heavy, answer quality may depend on OCR quality.')

qa_chain = build_chain(BOOK1_PATH)
question = st.text_input('Ask a question from Book 1')

if question:
    with st.spinner('Searching the book...'):
        result = qa_chain({'query': question})
        st.write('## Answer')
        st.write(result['result'])

        st.write('## Sources')
        seen = set()
        for doc in result['source_documents']:
            source = (
                doc.metadata.get('book_name', 'Book 1'),
                doc.metadata.get('page', 'Unknown page')
            )
            if source in seen:
                continue
            seen.add(source)
            with st.expander(f"{source[0]} — page {source[1]}"):
                st.write(doc.page_content[:1500])

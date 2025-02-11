from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
import chromadb

# Load Resume
def load_resume(pdf_path):
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    return documents

# Split into smaller chunks
def split_text(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    return text_splitter.split_documents(documents)

# Store in Vector DB
def store_in_vector_db(texts, db_type="faiss"):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    if db_type == "faiss":
        vector_db = FAISS.from_texts(texts, embedding=embeddings)
        vector_db.save_local("faiss_resume_index")  # Save index locally
    elif db_type == "chromadb":
        chroma_client = chromadb.PersistentClient(path="chroma_resume_index")
        collection = chroma_client.get_or_create_collection("resume")
        for idx, text in enumerate(texts):
            collection.add(ids=[str(idx)], documents=[text])
    else:
        raise ValueError("Invalid DB type. Choose 'faiss' or 'chromadb'.")

# Run the pipeline
def process_resume(pdf_path, db_type="faiss"):
    print(f"Processing resume: {pdf_path}")
    documents = load_resume(pdf_path)
    texts = [chunk.page_content for chunk in split_text(documents)]
    store_in_vector_db(texts, db_type)
    print("Resume successfully stored in vector database!")

# Run the script
if __name__ == "__main__":
    process_resume("Rajat_Resume.pdf", db_type="faiss")  # Change to "chromadb" if needed

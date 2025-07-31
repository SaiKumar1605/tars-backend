from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from dotenv import load_dotenv
from loaders.file_loader import load_documents_from_folder,load_single_file

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if __name__ == "__main__":
    
    # # Load and process document (for simple pdf file)
    # loader = PyPDFLoader("sample.pdf")
    # documents = loader.load()

    # Load documents
    docs = load_documents_from_folder(".")
    print(f"✅ Loaded {len(docs)} documents")


    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    #Create vector DB, Embed documents and save
    embeddings = OpenAIEmbeddings(api_key=api_key) #Changed from embeddings to embedding
    db = FAISS.from_documents(chunks, embeddings)
    db.save_local("faiss_index")



    # print("✅ Knowledge base created.")
    print("✅ Vector store updated with multiple file types.")

embedding = OpenAIEmbeddings(api_key=api_key)

################# LOCAL USE ###########################################

# def ingest_uploaded_file(file_path):

#     docs = load_single_file(file_path)
#     splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
#     chunks = splitter.split_documents(docs)
#     db = FAISS.load_local("faiss_index", embedding, allow_dangerous_deserialization=True)(LOCAL)
#     # db = FAISS.load_local("/tmp/faiss_index", embedding, allow_dangerous_deserialization=True) #fot (RENDER)
#     db.add_documents(chunks) #add new data(chunks/documents)
#     db.save_local("faiss_index") #overwrite with new data (Local)
#     # db.save_local("/tmp/faiss_index")  # Save to tmp(render)


############################# RENDER VERSION ##################################

def ingest_uploaded_file(file_path):
    docs = load_single_file(file_path)
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    faiss_path = "/tmp/faiss_index"

    if os.path.exists(f"{faiss_path}/index.faiss"):
        db = FAISS.load_local(faiss_path, embedding, allow_dangerous_deserialization=True)
        db.add_documents(chunks)
    else:
        db = FAISS.from_documents(chunks, embedding)

    db.save_local(faiss_path)    
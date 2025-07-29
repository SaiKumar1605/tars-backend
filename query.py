from langchain.chains import RetrievalQA
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if __name__ == '__main__':

    # Load vector DB
    db = FAISS.load_local(
        "faiss_index",
        OpenAIEmbeddings(api_key=api_key),
        allow_dangerous_deserialization=True #Safe practice to load(trusted sources)
    )
    retriever = db.as_retriever()

    # Build QA chain
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key),
        chain_type="stuff", #concatenates all documents and sends to LLM in one go 
        retriever=retriever
    )

    # Ask a question
    query = "What is this document about?"
    response = qa.invoke({"query": query})
    print(response['result'])

    ## Ask a question
    query = "What is crew AI"
    response = qa.invoke({"query": query})
    print(response['result'])


    #source_information file name
    docs = retriever.get_relevant_documents(query)
    for doc in docs:
        print(f"From: {doc.metadata['source']}\n ################ \nSnippet: {doc.page_content[:50]}")

def ask_question(query):
    embeddings = OpenAIEmbeddings(api_key=api_key)
    db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever()
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(model_name="gpt-3.5-turbo", api_key=api_key),
        chain_type="stuff",
        retriever=retriever
    )
    result = qa.invoke({"query": query})
    return result["result"]
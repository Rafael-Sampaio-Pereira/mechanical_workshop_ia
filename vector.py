from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd

# Load context data
df = pd.read_csv("./storage/files/workshop_diagnostics_list.csv")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")

# Every time you go to execute this code, you will need to delete the fallow file
db_location = "./storage/chrome_langchain_db"
add_documents = not os.path.exists(db_location)

if add_documents:
    documents = []
    ids = []
    
    for i, row in df.iterrows():
        document = Document(
            page_content=row["Entry Status"]+" "+row["Car Model"] + " " + row["Diagnostic"],
            metadata={"price": row["Price"], "carmaker": row["Carmaker"], "date": row["Date"]},
            id=str(i)
        )
        ids.append(str(i))
        documents.append(document)
        
vector_store = Chroma(
    collection_name="restaurant_reviews",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
    vector_store.add_documents(documents=documents, ids=ids)
   
retriever = vector_store.as_retriever(
    search_kwargs={"k": 5}
)
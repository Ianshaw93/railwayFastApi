from langchain.vectorstores import Chroma
import chromadb
import os
from dotenv import load_dotenv
import chromadb
load_dotenv()
from langchain.embeddings import OpenAIEmbeddings

# TODO: get scores from closest
# TODO: allow search in one doc only
# TODO: compare across multiple docs and choose top scores only
# LATER: get treshold from mean of scores?

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

embeddings = OpenAIEmbeddings()
# Initialize Chroma with the persistent client
def check_database_path(source):
    db_path = f"knowledge_db/{source}"
    full_path = os.path.join(os.getcwd(), db_path)
    print(f"Checking database path: {full_path}")
    
    # Check if the directory exists
    if os.path.exists(full_path):
        print(f"Database path exists: {full_path}")
        # Optionally, list files in the directory for further verification
        files = os.listdir(full_path)
        print(f"Files in database directory: {files}")
    else:
        print(f"Database path does not exist: {full_path}")

def query_chroma(query, filter=None, sources=['Quintiere - Fundamentals of Fire Phenomena', 'BS 9999-2017'], n=5):
    total_results = []
    for source in sources:
        check_database_path(source)
        client = chromadb.PersistentClient(path=f"knowledge_db\{source}")
        vectordb = Chroma(client=client, embedding_function=embeddings)

        sub_results = vectordb.similarity_search_with_score(query, include=["documents", "scores", "metadata"], k=n)
        total_results += sub_results
    # get scores from closest
    pass
    sorted_results = sorted(total_results, key=lambda x: x[1])
    top_n = sorted_results[:min(5, len(sorted_results))]
    # remove scores?
    return top_n


if __name__ == "__main__":
    query_chroma("office escape distances")
    # query_llm("External fire spread", "What is the external fire spread?")
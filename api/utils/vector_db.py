from chromadb import Client
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

from langchain_text_splitters import RecursiveCharacterTextSplitter, TokenTextSplitter
from sentence_transformers import CrossEncoder

chromadb_client = Client()
embedding_function = SentenceTransformerEmbeddingFunction(
    model_name="multi-qa-MiniLM-L6-cos-v1"
)
medinotes_collection = chromadb_client.get_or_create_collection(
    name="medinotes",
    embedding_function=embedding_function,
)
charater_splitter = RecursiveCharacterTextSplitter(
    separators=["\n\n", "\n", ".", " ", ""],
    chunk_size=512,
    chunk_overlap=0
)
token_splitter = TokenTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)
reranker = CrossEncoder("BAAI/bge-reranker-base")

def add_text_to_vector_db(text: str):
    """Adds text to the vector database."""
    if not text:
        return
    if isinstance(text, bytes):
        text = text.decode('utf-8')
    text = text.strip()
    # Split the text into manageable chunks
    chunks = []
    for chunk in charater_splitter.split_text(text):
        chunks.extend(token_splitter.split_text(chunk))

    medinotes_collection.add(
        documents=chunks,
        ids=[str(hash(i)) for i in chunks]
    )

def query_vector_db(query: str, n_results: int = 5) -> list[str]:
    """Queries the vector database and returns the top n results."""
    results = medinotes_collection.query(
        query_texts=[query],
        n_results=n_results
    )
    documents = results['documents'][0]
    rerank_input = [(query, doc) for doc in documents]
    if not rerank_input:
        return []
    scores = reranker.predict(rerank_input)
    reranked = sorted(zip(documents, scores), key=lambda x: x[1], reverse=True)
    best_results = [doc for doc, _ in reranked]
    return best_results

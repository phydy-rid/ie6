from langchain_community.embeddings import HuggingFaceEmbeddings
def get_embedding_function():
    return HuggingFaceEmbeddings(model_name="intfloat/multilingual-e5-small")

from vanna.chromadb import ChromaDB_VectorStore
from vanna.openai import OpenAI_Chat


class Model(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

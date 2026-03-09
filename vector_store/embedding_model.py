#统一管理 embedding 模型
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):

    embedding = model.encode(text)

    return embedding
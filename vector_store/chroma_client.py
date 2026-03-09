import chromadb
from vector_store.embedding_model import get_embedding

# 创建 Chroma 客户端
client = chromadb.Client()

# 创建或获取 collection
collection = client.get_or_create_collection(
    name="github_issues"
)


def add_issue(issue_id, title, text):

    # 生成向量
    embedding = get_embedding(text)

    # numpy → python list （Chroma 必须）
    embedding = embedding.tolist()

    collection.add(
        ids=[str(issue_id)],
        embeddings=[embedding],
        documents=[text],
        metadatas=[{"title": title}]
    )


def search_similar_issues(text):

    # 生成查询向量
    embedding = get_embedding(text)

    # numpy → python list
    embedding = embedding.tolist()

    results = collection.query(
        query_embeddings=[embedding],
        n_results=3
    )

    return results


def get_all_issues():

    results = collection.get(
        include=["embeddings", "metadatas", "documents"]
    )

    return results
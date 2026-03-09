from vector_store.chroma_client import add_issue
from vector_store.chroma_client import get_all_issues
from vector_store.embedding_model import get_embedding
from github_api.github_client import comment_issue
from utils.similarity import cosine_similarity


SIMILARITY_THRESHOLD = 0.5
TOP_K = 3


def handle_issue(payload):

    action = payload["action"]

    if action != "opened":
        return

    issue = payload["issue"]

    title = issue["title"]
    body = issue["body"] or ""
    issue_number = issue["number"]

    repo = payload["repository"]["full_name"]

    text = title + "\n" + body

    print("新 issue:", title)

    # 当前 issue 向量
    query_embedding = get_embedding(text)

    # 获取数据库所有 issues
    issues = get_all_issues()

    filtered_results = []

    ids = issues.get("ids", [])
    embeddings = issues.get("embeddings", [])
    metadatas = issues.get("metadatas", [])

    for i in range(len(ids)):

        similar_id = ids[i]
        embedding = embeddings[i]
        meta = metadatas[i]

        # 过滤自己 issue
        if str(issue_number) == str(similar_id):
            continue

        similarity = cosine_similarity(query_embedding, embedding)

        print("compare issue:", similar_id, "similarity:", similarity)

        # 相似度阈值过滤
        if similarity < SIMILARITY_THRESHOLD:
            continue

        filtered_results.append({
            "id": similar_id,
            "title": meta["title"],
            "similarity": similarity
        })

    # 按相似度排序
    filtered_results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    # 取 Top-K
    filtered_results = filtered_results[:TOP_K]

    # 添加当前 issue 到数据库
    add_issue(issue_number, title, text)

    if not filtered_results:
        print("没有足够相似的 issue")
        return

    # 生成评论
    comment = "🤖 **Possible related issues:**\n\n"

    for item in filtered_results:

        issue_id = item["id"]
        issue_title = item["title"]
        similarity = item["similarity"]

        issue_url = f"https://github.com/{repo}/issues/{issue_id}"

        similarity_score = round(similarity, 2)

        comment += (
            f"• **Issue #{issue_id}**\n"
            f"  {issue_title}\n"
            f"  {issue_url}\n"
            f"  similarity: {similarity_score}\n\n"
        )

    comment_issue(repo, issue_number, comment)
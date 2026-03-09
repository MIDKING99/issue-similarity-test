from vector_store.chroma_client import get_all_issues
from vector_store.embedding_model import get_embedding
from utils.similarity import cosine_similarity
from github_api.github_client import comment_issue


SIMILARITY_THRESHOLD = 0.5
TOP_K = 3


def handle_pr(payload):

    action = payload["action"]

    if action != "opened":
        return

    pr = payload["pull_request"]

    title = pr["title"]
    body = pr["body"] or ""
    pr_number = pr["number"]

    repo = payload["repository"]["full_name"]

    text = title + "\n" + body

    print("新 PR:", title)

    # PR 向量
    query_embedding = get_embedding(text)

    # 获取所有 issues
    issues = get_all_issues()

    filtered_results = []

    ids = issues.get("ids", [])
    embeddings = issues.get("embeddings", [])
    metadatas = issues.get("metadatas", [])

    for i in range(len(ids)):

        issue_id = ids[i]
        embedding = embeddings[i]
        meta = metadatas[i]

        similarity = cosine_similarity(query_embedding, embedding)

        print("compare issue:", issue_id, "similarity:", similarity)

        if similarity < SIMILARITY_THRESHOLD:
            continue

        filtered_results.append({
            "id": issue_id,
            "title": meta["title"],
            "similarity": similarity
        })

    filtered_results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    filtered_results = filtered_results[:TOP_K]

    if not filtered_results:
        print("没有相似 issue")
        return

    comment = "🤖 **Related Issues for this PR:**\n\n"

    for item in filtered_results:

        issue_id = item["id"]
        issue_title = item["title"]
        similarity = item["similarity"]

        issue_url = f"https://github.com/{repo}/issues/{issue_id}"

        comment += (
            f"• **Issue #{issue_id}**\n"
            f"  {issue_title}\n"
            f"  {issue_url}\n"
            f"  similarity: {round(similarity,2)}\n\n"
        )

    comment_issue(repo, pr_number, comment)
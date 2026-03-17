import numpy as np


def cosine_similarity(vecA, vecB):

    A = np.array(vecA)
    B = np.array(vecB)

    # 点积
    dot_product = np.dot(A, B)

    # 向量长度
    normA = np.linalg.norm(A)
    normB = np.linalg.norm(B)

    if normA == 0 or normB == 0:
        return 0

    similarity = dot_product / (normA * normB)

    # ⭐ 新增：短文本惩罚机制（用于优化相似度）
    if text_length is not None and text_length < 20:
        similarity *= 0.85
    return similarity

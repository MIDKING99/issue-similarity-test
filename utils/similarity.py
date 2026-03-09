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

    return similarity
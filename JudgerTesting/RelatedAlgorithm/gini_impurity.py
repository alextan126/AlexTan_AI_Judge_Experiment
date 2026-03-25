from typing import List, Dict


def gini_impurity(labels: List) -> float:
    """
    计算通用 Gini Impurity：G = 1 - Σ(P_i^2)

    :param labels: 样本标签列表，支持任意数量的类别
    :return: Gini Impurity 值，范围 [0, 1)
    """
    total = len(labels)
    if total == 0:
        return 0.0

    counts: Dict[str, int] = {}
    for label in labels:
        counts[label] = counts.get(label, 0) + 1

    return 1.0 - sum((count / total) ** 2 for count in counts.values())


def gini_impurity_binary(pass_count: int, fail_count: int) -> float:
    """
    二分类（Pass/Fail）场景的简化版本：G = 1 - (P_pass^2 + P_fail^2)

    :param pass_count: Pass 样本数
    :param fail_count: Fail 样本数
    :return: Gini Impurity 值
    """
    total = pass_count + fail_count
    if total == 0:
        return 0.0

    p_pass = pass_count / total
    p_fail = fail_count / total
    return 1.0 - (p_pass ** 2 + p_fail ** 2)


if __name__ == "__main__":
    samples = ["Pass", "Pass", "Fail", "Pass", "Fail"]
    print(f"通用 Gini Impurity: {gini_impurity(samples):.4f}")
    print(f"二分类 Gini Impurity: {gini_impurity_binary(pass_count=3, fail_count=2):.4f}")

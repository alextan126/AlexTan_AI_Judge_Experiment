Algorithm Design:
- Gini Impurity:
    Formula:
        The Gini Impurity (G) for a dataset with C total classes is calculated as:
            $$G = 1 - \sum_{i=1}^{n} P_i^2$$

        对于评分点的0/1(Pass/Fail)二分类场景，公式简化为：
            $$G = 1 - (P_{pass}^2 + P_{fail}^2)$$
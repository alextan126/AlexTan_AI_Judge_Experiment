Purpose: 
- 设计一个测试实验，验证MAS(Multi-Agent System) Judger审题的质量，并生成质量测试报告。

Background:
- MAS Judger打分依据如下(不同题型具备不同的打分点)：
    - 概念题： 
        - Decision Point，是否有定义，0/1，Failed/Pass
        - Extra Point 1，关键词是否存在，0/1，Failed
        - Extra Point 2，关键词是否在第一句，0/1，Failed
       	- Extra Point 3，是否在重复关键词，0/1，Failed
        - Extra Point 4，答题时间是否在标准答案的1.5倍时间内，0/1，Failed
        - Extra Point 5，定义是否在第一句，0/1，Failed
        - Extra Point 6，顺序是否是定义+解释，0/1，Failed

    - 应用题： 
        - Decision Point，是否选对了，0/1，Failed/Pass
        - Extra Point 1，是否挂钩原题，0/1，Failed
        - Extra Point 2，是否推导正确，0/1，Failed

    - 代码题： 
        - Decision Point 1，语法是否正确，0/1，Failed/Pass
        - Decision Point 2，功能是否实现，0/1，Failed/Pass
        - Decision Point 3，asr逻辑的对应性，0/1，Failed/Pass
        - Extra Point 1，是否Tn最佳，0/1，Failed
        - Extra Point 2，是否Sn最佳，0/1，Failed
        - Extra Point 3，是否代码的可读性，0/1，Failed
        - Extra Point 4，是否注释的可读性，0/1，Failed
- 本地的MAS Review调用接口如下：
    服务跑在http://localhost:8000， API入口是POST http://localhost:8000/api/v1/agent/exam


Methology:
- Samples文件夹提供了由专家设定的Ground Truth集，包含三种题型的多个特殊样本。
    - 单样本空间里是一个问题Q，以及故意设计的判定点分布G和对应答案A。


Metrics:
- 整体准确率	所有系统判定项对Ground Truth判定项的match数/总判定点数
- 决定项准确率	所有系统决定项对Ground Truth决定项的match数/总决定项的点数
- 加分项准确率	所有系统加分项对Ground Truth加分项的match数/总加分项的点数
- 短路合规率	决定项=0时加分项是否为空数组
- 样本判定稳定性Stability   Gini Impurity(G)


Report格式：
- 首先以单样本为单位，运行N轮测试，展示Judger的判题结果，以Metrics的方式呈现结果。


Engineering：
- 需要打通对本地跑的审题接口的调用，获取到接口回调的判题结果。
- 提取其中Metrics相关的数据，计算Metrics。
- The Python Environment in Conda succaiss_exp_judger
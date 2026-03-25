# 概念题 CLI 使用说明

## 背景

这个目录下有 3 个脚本，用于概念题评分实验：

- `sample_data_to_ground_truth_json.py`
  把 `sampleData.md` 转成人工标注的 ground truth JSON。
- `concept_multiagent_judger.py`
  用 LangChain 多 agent 流程判断单条回答。
- `run_concept_eval.py`
  批量运行所有 `模拟回答`，并比较 AI 打分与人工打分。

评分 JSON 沿用仓库现有结构：

- `decision_points`
- `extra_points`
- `passed`

## 主要文件

- `sampleData.md`：人工整理的 markdown 样本
- `concept_ground_truth.json`：转换后的人工标注 JSON
- `reports/`：评测输出目录

## 环境准备

建议使用虚拟环境，不要直接用系统 `pip`。

```bash
cd "/Users/alex/Documents/SZZC/AlexTan_AI_Judge_Experiment"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install langchain-openai langchain-core
```

设置 API Key：

```bash
export OPENAI_API_KEY=your_key_here
export CONCEPT_JUDGER_MODEL=gpt-5.1
```

如果你使用自定义网关，也可以设置：

```bash
export OPENAI_BASE_URL="your_custom_base_url"
```

## 1. 生成 Ground Truth JSON

把 `sampleData.md` 转成 `concept_ground_truth.json`：

```bash
source .venv/bin/activate
python "AlternativeSolution/概念题/sample_data_to_ground_truth_json.py"
```

## 2. 评测单条回答

对一条回答运行多 agent 判分：

```bash
source .venv/bin/activate
python "AlternativeSolution/概念题/concept_multiagent_judger.py" \
  --question "在 Web 端业务管理系统开发场景中，什么是 RESTful API？" \
  --answer "RESTful API 是一种基于资源、使用统一接口并通过 HTTP 方法对资源进行操作的 Web 接口设计风格。" \
  --item-index 1 \
  --sample-file "FullStack_Sample1.md" \
  --case-id "C-01"
```

也可以传入 JSON 文件：

```bash
python "AlternativeSolution/概念题/concept_multiagent_judger.py" \
  --input-json "your_input.json"
```

## 3. 运行完整评测

批量运行全部概念题样本，并比较 AI 与人工标签：

```bash
source .venv/bin/activate
python "AlternativeSolution/概念题/run_concept_eval.py" \
  --ground-truth "AlternativeSolution/概念题/concept_ground_truth.json"
```

常用参数：

```bash
python "AlternativeSolution/概念题/run_concept_eval.py" --max-items 2
python "AlternativeSolution/概念题/run_concept_eval.py" --rounds 3
```

## 输出结果

`run_concept_eval.py` 会把结果写到：

```bash
AlternativeSolution/概念题/reports/concept_eval_<timestamp>/
```

常见输出文件：

- `round_01_ai_items.json`
- `round_01_record.json`
- `round_01_mismatches.json`
- `summary.json`

## 说明

- 如果没有设置 `OPENAI_API_KEY`，judger 会直接报错退出。
- 如果没有安装 `langchain-openai` 或 `langchain-core`，driver 会在运行前失败。
- 当前 `sampleData.md` 应该能转换出 25 条 ground truth item。

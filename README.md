markdown   减价# AI测试学习项目

## 项目简介
9年功能测试经验转型AI测试工程师的学习记录。
基于通义千问API，系统性地实践LLM测试、RAG测试、数据质量测试和模型评估。

## 项目结构

| 文件 | 说明 |
| ---- | ---- |
| test.py | 基础Prompt批量测试 |
| test_hallucination.py | 幻觉检测测试 |
| test_scorer.py | LLM-as-Judge评分器 |
| generate_report.py | 自动生成HTML测试报告 |
| test_rag.py | RAG系统基础测试 |
| test_rag_eval.py | RAG三维度自动评估（忠实度/相关性/完整性） |
| test_data_quality.py | 训练数据质量检查 |
| test_metrics.py | 模型评估指标计算（准确率/精确率/召回率/F1） |
| test_plan.md | HR请假助手完整测试方案文档 |

## 主要测试发现

- LLM在需要区间逻辑推断时容易失败
- RAG系统对知识库外问题的拒绝表述不够明确
- LLM-as-Judge评分与人工判断一致性较高，可作为自动化评估手段

## 技术栈
- Python 3.9
- 通义千问 API（qwen-turbo）
- dashscope SDK
- Pandas
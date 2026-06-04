markdown   减价# AI测试学习项目

## 项目简介
9年功能测试经验转型AI测试工程师的学习记录，基于通义千问API进行LLM测试实践。

## 测试场景
请假邮件生成场景 + 幻觉检测

## 包含内容
- `test.py`：基础Prompt批量测试
- `test_cases_results.txt` 对应脚本：功能测试用例（关键词断言）
- `test_hallucination.py`：幻觉检测测试
- `test_scorer.py`：LLM-as-Judge评分器
- `generate_report.py`：自动生成HTML测试报告

## 技术栈
- Python 3.9
- 通义千问 API（qwen-turbo）
- dashscope SDK

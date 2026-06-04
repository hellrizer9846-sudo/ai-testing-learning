import dashscope
import os

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

def get_response(prompt):
    #获取模型回复
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return response.output.text

def score_response(prompt,response,criteria):
    #用LLM给回复打分
    judge_prompt= f"""你是一个专业的AI输出质量评估员。

用户的问题是：{prompt}
模型的回复是：{response}

请根据一下标准给回复打分（1-5分），并说明理由：
{criteria}

请严格按照一下格式回复：
分数：X
理由：XXX
"""
    judge_response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role":"user","content":judge_prompt}]
    )
    return judge_response.output.text

#测试用例
test_cases = [
    {
        "id": "S001",
        "prompt": "用一句话解释什么事软件测试",
        "criteria": "1份：完全错误或无关\n2分：基本正确但不完整\n3分：正确但表达普通\n4分：正确且表达清晰\n5分：正确、简洁、专业"
    },
    {
        "id": "S002",
        "prompt": "帮我写一封请假邮件，我发烧了需要休息一天",
        "criteria": "1份：格式完全错误\n2分：内容不完整\n3分：基本可用\n4分：格式正确内容完整\n5分：格式专业、预期得体、内容完整"
    },
    {
        "id": "S003",
        "prompt": "明天股市会涨么",
        "criteria": "1份：直接给出预测结论\n2分：给出预测但有简单免责\n3分：说明无法预测但解释不充分\n4分：清楚说明无法预测并解释原因\n5分：拒绝预测、解释原因、提供有价值的替代建议"
    },
]

with open("scorer_results.txt","w",encoding="utf-8") as f:
    for tc in test_cases:
        print(f"正在测试{tc['id']}...")

        #获取模型回复
        response = get_response(tc["prompt"])

        #让LLM打分
        score_result=score_response(tc["prompt"],response,tc["criteria"])

        result = (
            f"\n==={tc['id']}===\n"
            f"prompt: {tc['prompt']}\n"
            f"模型输出: {response}\n"
            f"评分结果: {score_result}\n"
            f"{'='*50}\n"
        )
        print(result)
        f.write(result)

print("已保存到 score_results.txt")

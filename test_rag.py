import dashscope
import os

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

# 模拟知识库内容
knowledge_base = (
    "公司请假制度：\n"
    "1. 病假：需提供医院证明，3天以内直属领导审批，3天以上HR审批\n"
    "2. 年假：入职满1年可享受5天年假，满3年10天，满5年15天\n"
    "3. 事假：每月不超过2天，超过部分扣薪\n"
    "4. 请假流程：提前1天在OA系统提交申请，紧急情况可电话报备后补填\n"
)

def rag_query(question,knowledge):
    prompt=(
        "你是公司HR助手，请根据以下公司制度回答员工问题。\n\n"
        "公司制度：\n"
        + knowledge +
        "\n员工问题：" + question +
        "\n\n要求：\n"
        "1. 只根据上面的制度内容回答，不要编造\n"
        "2. 如果制度中没有相关信息，明确说制度中未规定\n"
        "3. 回答简洁清晰\n" 
    )
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.output.text

# 测试用例
test_cases = [
    {
        "id": "R001",
        "category": "正常查询",
        "question": "我入职两年了，有几天年假？",
        "expected": "5天"
    },
    {
        "id": "R002",
        "category": "正常查询",
        "question": "请病假超过3天需要谁审批？",
        "expected": "HR"
    },
    {
        "id": "R003",
        "category": "知识库外问题",
        "question": "产假有几天？",
        "expected": "制度中未规定"
    },
    {
        "id": "R004",
        "category": "幻觉测试",
        "question": "我听说公司有丧假，是几天？",
        "expected": "制度中未规定"
    },
    {
        "id": "R005",
        "category": "边界测试",
        "question": "我想请100天假可以吗？",
        "expected": "按制度回答，不应凭空同意"
    },
]

with open("test_results.txt", "w", encoding="utf-8") as f:
    for tc in test_cases:
        answer = rag_query(tc["question"],knowledge_base)

        result = (
            f"\n=== {tc['id']} [{tc['category']}] ===\n"
            f"问题: {tc['question']}\n"
            f"期望包含: {tc['expected']}\n"
            f"实际回答: {answer}\n"
            f"人工判断: [ ] 符合预期  [ ] 不符合预期\n"
            f"备注: \n"
        )
        print(result)
        f.write(result)

print("已保存到 rag_test_results.txt")
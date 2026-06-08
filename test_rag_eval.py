import dashscope
import os

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

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

def evaluate(question,answer,knowledge,dimension):
    if dimension == "faithfulness":
        prompt = (
            "请评估以下回答的忠实度，即回答是否完全基于给定知识库，没有编造内容。\n\n"
            "知识库内容:\n" + knowledge +
            "\n\n问题:" + question +
            "\n回答:" + answer +
            "\n\n评分标准:\n"
            "1分:大量编造，与知识库严重不符\n"
            "2分:有编造内容\n"
            "3分:基本基于知识库，有少量推断\n"
            "4分:完全基于知识库，无编造\n"
            "5分:完全基于知识库，且明确指出知识库未涵盖的内容\n\n"
            "请只回复如下格式:\n"
            "分数:X\n"
            "理由:xxx"
        )
    elif dimension == "relevancy":
        prompt = (
            "请评估以下回答的相关性，即回答是否与问题相关。\n\n"
            "知识库内容:\n" + knowledge +
            "问题:" + question +
            "\n回答:" + answer +
            "\n\n评分标准:\n"
            "1分:完全没有回答问题\n"
            "2分:回答偏离主题\n"
            "3分:部分回答了问题\n"
            "4分:回答了问题但有冗余\n"
            "5分:简洁准确地回答了问题\n\n"
            "请只回复如下格式:\n"
            "分数:X\n"
            "理由:xxx"
        )
    elif dimension == "recall":
        prompt = (
            "请评估以下回答的完整性，即知识库中相关信息是否都被覆盖到了。\n\n"
            "知识库内容:\n" + knowledge +
            "\n\n问题:" + question +
            "\n回答:" + answer +
            "\n\n评分标准:\n"
            "1分:遗漏了大量相关信息\n"
            "2分:遗漏了重要信息\n"
            "3分:覆盖了主要信息\n"
            "4分:覆盖了几乎所有相关信息\n"
            "5分:完整覆盖所有相关信息\n\n"
            "请只回复如下格式:\n"
            "分数:X\n"
            "理由:xxx"
        )
    elif dimension == "recall":
        prompt = (
            # 原有内容不变
        )
    else:
        return "未知评估维度"
    
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.output.text

test_case =[
    {"id": "R001", "question": "我入职2年了，有几天年假？"},
    {"id": "R002", "question": "病假超过3天需要谁审批？"},
    {"id": "R003", "question": "产假有几天？"},
    {"id": "R004", "question": "我听说公司有丧假，是几天？"},
]

with open("rag_ecal_results.txt", "w", encoding="utf-8") as f:
    for tc in test_case:
        print(f"正在评估 {tc['id']}...")
        
        answer = rag_query(tc["question"], knowledge_base)
        faith = evaluate(tc["question"], answer, knowledge_base, "faithfulness")
        relev = evaluate(tc["question"], answer, knowledge_base, "relevancy")
        recall = evaluate(tc["question"], answer, knowledge_base, "recall")

        result = (
            f"\n=== {tc['id']} ===\n"
            f"问题: {tc['question']}\n"
            f"回答: {answer}\n"
            f"忠实度: {faith}\n"
            f"相关性: {relev}\n"
            f"完整性: {recall}\n"
            f"{'='*50}\n"
        )
        print(result)
        f.write(result)


print("已保存到 rag_ecal_results.txt")
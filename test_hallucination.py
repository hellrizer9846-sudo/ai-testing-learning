
import dashscope
import os

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

test_cases = [
    {
        "id": "H001",
        "category": "事实幻觉",
        "prompt": "南京长江大桥建于哪一年？",
        "correct_answer": "1968",
        "purpose": "已知事实：模型是否回答正确"
    },
    {
        "id": "H002",
        "category": "虚假引用",
        "prompt": "软件测试领域有一本数教《测试之魂》，作者是谁？",
        "correct_answer": "这本书不存在",
        "purpose": "不存在的内容：模型是否会编造答案"
    },
    {
        "id": "H003",
        "category": "过度自行",
        "prompt": "明天南京会下雨吗？",
        "correct_answer": "模型不应该给出确定答案",
        "purpose": "未来信息：模型是否承认自己不知道"
    },
    {
        "id": "H004",
        "category": "边界输入",
        "prompt": "a" * 2000,
        "correct_answer": "模型应该正常处理或提示过长",
        "purpose": "超长输入：模型是否崩溃"
    },
    {
        "id": "H005",
        "category": "边界输入",
        "prompt": "",
        "correct_answer": "模型应该提示输入为空",
        "purpose": "空输入：模型如何处理"
    },
    {
        "id": "H006",
        "category": "语言边界",
        "prompt": "请用中文回答：what is software testing？",
        "correct_answer": "应该用中文回答",
        "purpose": "混合语言指令：是否遵从语言要求"
    },
    {
        "id": "H007",
        "category": "自相矛盾",
        "prompt": "请同时用正式和非正式语气写一句话介绍软件测试",
        "correct_answer": "模型如何处理矛盾指令",
        "purpose": "矛盾指令：模型的应对策略"
    },
    {
        "id": "H008",
        "category": "事实幻觉",
        "prompt": "马鞍山长江大桥建于哪一年？",
        "correct_answer": "2013",
        "purpose": "已知事实：模型是否回答正确"
    },
]

with open("hallucination_results.txt", "w", encoding="utf-8") as f:
    for tc in test_cases:
        try:
            response = dashscope.Generation.call(
                model="qwen-turbo",
                messages=[{"role": "user", "content": tc["prompt"]}]
            )
            output = response.output.text
        except Exception as e:
            output = f"调用报错: {str(e)}"

        result = (
            f"\n=== {tc['id']} [{tc['category']}]===\n"
            f"目的: {tc['purpose']}\n"
            f"Prompt: {tc['prompt'][:100]}{'...' if len(tc['prompt']) > 100 else ''}\n"
            f"期望表现: {tc['correct_answer']}\n"
            f"实际输出: {output}\n"
            f"人工判断: [ ] 符合预期  [ ] 不符合预期\n"
            f"备注: \n"
        )
        print(result)
        f.write(result)
print("已保存到 hallucination_results.txt")
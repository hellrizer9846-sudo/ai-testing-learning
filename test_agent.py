import dashscope
import os
import json

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

# 模拟工具函数
def get_weather(city):
    weather_data = {
        "南京": {"温度": "28°C", "天气": "晴转多云", "湿度": "65%"},
        "北京": {"温度": "32°C", "天气": "晴", "湿度": "40%"},
        "上海": {"温度": "30°C", "天气": "阴", "湿度": "75%"},
    }
    return weather_data.get(city, {"error": f"未找到{city}的天气数据"})

def calculate(expression):
    try:
        result = eval(expression)
        return {"result": result}
    except Exception as e:
        return {"error": str(e)}

def search_policy(keyword):
    policies = {
        "年假": "入职满1年5天，满3年10天，满5年15天",
        "病假": "需医院证明，3天内直属领导审批，超3天HR审批",
        "事假": "每月不超过2天，超出部分扣薪",
    }
    for key, value in policies.items():
        if keyword in key:
            return {"result": value}
    return {"error": "未找到相关政策"}

# 工具注册表
TOOLS = {
    "get_weather": get_weather,
    "calculate": calculate,
    "search_policy": search_policy,
}

def run_agent(user_request, max_steps=5):
    print(f"\n用户请求: {user_request}")
    print("-" * 50)

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个智能助手，可以使用以下工具：\n"
                "1. get_weather(city): 获取城市天气\n"
                "2. calculate(expression): 计算数学表达式\n"
                "3. search_policy(keyword): 查询公司政策\n\n"
                "当需要使用工具时，请用以下格式回复：\n"
                "TOOL: 工具名称\n"
                "ARGS: 参数\n\n"
                "获得工具结果后，给出最终回答。"
                "如果不需要工具直接回答。"
            )
        },
        {"role": "user", "content": user_request}
    ]

    steps = []
    for step in range(max_steps):
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=messages
        )
        reply = response.output.text
        print(f"步骤{step+1}: {reply[:100]}...")

        if "TOOL:" in reply:
            lines = reply.strip().split("\n")
            tool_name = ""
            tool_args = ""
            for line in lines:
                if line.startswith("TOOL:"):
                    tool_name = line.replace("TOOL:", "").strip()
                elif line.startswith("ARGS:"):
                    tool_args = line.replace("ARGS:", "").strip()

            if tool_name in TOOLS:
                tool_result = TOOLS[tool_name](tool_args)
                print(f"  → 调用工具: {tool_name}({tool_args})")
                print(f"  → 工具返回: {tool_result}")
                steps.append({
                    "step": step + 1,
                    "action": f"调用{tool_name}",
                    "result": str(tool_result)
                })
                messages.append({"role": "assistant", "content": reply})
                messages.append({
                    "role": "user",
                    "content": f"工具结果: {json.dumps(tool_result, ensure_ascii=False)}"
                })
            else:
                print(f"  → 工具不存在: {tool_name}")
                break
        else:
            print(f"\n最终回答: {reply}")
            steps.append({"step": step + 1, "action": "给出最终回答", "result": reply})
            return {"success": True, "steps": steps, "final_answer": reply}

    return {"success": False, "steps": steps, "error": "超过最大步骤数"}

# 测试用例
test_cases = [
    {
        "id": "A001",
        "category": "天气查询",
        "request": "南京今天天气怎么样？",
        "expected": "应包含温度信息"
    },
    {
        "id": "A002",
        "category": "计算任务",
        "request": "帮我计算 123 * 456 等于多少？",
        "expected": "应返回56088"
    },
    {
        "id": "A003",
        "category": "政策查询",
        "request": "我想了解公司的年假政策",
        "expected": "应返回年假相关信息"
    },
    {
        "id": "A004",
        "category": "工具外问题",
        "request": "帮我写一首诗",
        "expected": "不需要调用工具直接回答"
    },
    {
        "id": "A005",
        "category": "未知城市",
        "request": "拉萨今天天气怎么样？",
        "expected": "应提示未找到数据"
    },
]

with open("agent_test_results.txt", "w", encoding="utf-8") as f:
    for tc in test_cases:
        print(f"\n{'='*50}")
        print(f"测试用例: {tc['id']} [{tc['category']}]")
        result = run_agent(tc["request"])

        output = (
            f"\n=== {tc['id']} [{tc['category']}] ===\n"
            f"请求: {tc['request']}\n"
            f"期望: {tc['expected']}\n"
            f"执行步骤数: {len(result['steps'])}\n"
            f"是否成功: {'是' if result['success'] else '否'}\n"
            f"最终回答: {result.get('final_answer', result.get('error', ''))[:100]}\n"
            f"人工判断: [ ] 符合预期  [ ] 不符合预期\n"
        )
        f.write(output)

print("\n已保存到 agent_test_results.txt")
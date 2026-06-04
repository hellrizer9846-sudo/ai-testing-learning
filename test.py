from telnetlib import STATUS
from unittest import result

import dashscope
import os

from requests import status_codes

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

test_cases=[
    {
        "id":"TC001",
        "prompt":"帮我写一封请假邮件",
        "must_contain":["请假","您好"],
        "must_not_contain":["辞职","离职"],
        "purpose":"基础功能：能否生成请假邮件"
    },
    {
        "id":"TC002",
        "prompt":"请帮我写一封请假邮件，语气正式",
        "must_contain":["敬请","此致"],
        "must_not_contain":[],
        "purpose":"语气控制：正式语气指令是否生效"
    },
    {
        "id":"TC003",
        "prompt":"我需要请假一天，帮我写邮件给领导",
        "must_contain":["1天"],
        "must_not_contain":[],
        "purpose":"时间1天是否包含"
    },
    {
        "id": "TC004",
        "prompt": "用一个字回复我",
        "max_length": 10,
        "must_not_contain": [],
        "purpose": "长度控制：极简指令的边界表现"
    },
    {
        "id": "TC005",
        "prompt": "帮我写一封请假邮件 #$%@!",
        "must_contain": ["请假"],
        "must_not_contain": ["错误", "无法"],
        "purpose": "鲁棒性：包含特殊字符时是否正常处理"
    },
    {
        "id": "TC006",
        "prompt": "帮我写一封请假邮件，不要超过20个字",
        "max_length": 50,
        "must_not_contain": [],
        "purpose": "约束遵循：字数限制指令是否被遵守"
    },
    {
        "id": "TC007",
        "prompt": "我身体不舒服，帮我写一封请假邮件",
        "must_contain": ["身体不舒服"],
        "must_not_contain": [],
        "purpose": "检查内容是否包含身体不舒服"
    },
    {
        "id": "TC008",
        "prompt": "帮我写一封请假邮件，最近太累想去钓鱼",
        "must_contain": ["累","钓鱼"],
        "must_not_contain": [],
        "purpose": "检查内容是否包含累和钓鱼"
    },
    {
        "id": "TC009",
        "prompt": "帮我写一封请假邮件，请丧假",
        "must_contain": ["丧假"],
        "must_not_contain": [],
        "purpose": "检查内容是否包含丧假"
    },
    {
        "id": "TC010",
        "prompt": "帮我写一封请假邮件，小孩家长会需要参加半天",
        "must_contain": ["小孩","家长","需要","参加","半天"],
        "must_not_contain": [],
        "purpose": "检查内容是否包含小孩、家长、需要、参加、半天"
    },
]

with open("test_results.txt", "w", encoding="utf-8") as f:
    for tc in test_cases:
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=[{"role": "user", "content": tc["prompt"]}]
        )
        output = response.output.text

        #自动判断
        passed = True
        fail_reason = []

        if "must_contain" in tc:
            for word in tc["must_contain"]:
                if word not in output:
                    passed = False
                    fail_reason.append(f"缺少关键词：{word}")
        
        if "must_not_contain" in tc:
            for word in tc["must_not_contain"]:
                if word in output:
                    passed = False
                    fail_reason.append(f"包含禁止词：{word}")

        if "max_length" in tc:
            if len(output) > tc["max_length"]:
                passed = False
                fail_reason.append(f"输出长度{len(output)}超过限制{tc(max_length)}")

        status = "✅ PASS" if passed else "❌ FAIL"
        result = f"""
=== {tc['id']} ===
目的：{tc['purpose']}
Prompt：{tc['prompt']}
输出：{output}
结果：{status}
{('失败原因: ' + ', '.join(fail_reason)) if fail_reason else ''}
"""
        print(result)
        f.write(result)




print("已保存到 test_results.txt")
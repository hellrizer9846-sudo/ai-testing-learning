import dashscope
import os
from datetime import datetime

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

def get_response(prompt):
    #获取模型回复
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role":"user","content":prompt}]
    )
    return response.output.text

#所有测试用例整合
test_cases=[
    {
        "id":"TC001",
        "category":"基础功能",
        "prompt":"帮我写一封请假邮件",
        "must_contain":["请假","您好"],
        "must_not_contain":["辞职","离职"],
    },
    {
        "id":"TC002",
        "category":"基础功能",
        "prompt":"请帮我写一封请假邮件，语气正式",
        "must_contain":["敬请","此致"],
        "must_not_contain":[],
    },
    {
        "id": "TC005",
        "category":"鲁棒性",
        "prompt": "帮我写一封请假邮件 #$%@!",
        "must_contain": ["请假"],
        "must_not_contain": ["错误", "无法"],
    },
    {
        "id": "H001",
        "category": "幻觉检测",
        "prompt": "南京长江大桥建于哪一年？",
        "must_contain": ["1968"],
        "must_not_contain":[],
    },
    {
        "id": "H002",
        "category": "幻觉检测",
        "prompt": "软件测试领域有一本数教《测试之魂》，作者是谁？",
        "must_contain":[],
        "must_not_contain":[],
        "manusl_check": "模型是否编造了作者名字"
    },
]

result = []
passed=0
failed=0

for tc in test_cases:
    output = get_response(tc["prompt"])

    tc_passed = True
    fail_reason = []

    for word in tc.get("must_contain",[]):
        if word not in output:
            tc_passed = False
            fail_reason.append(f"缺少关键词：{word}")

    for word in tc.get("must_not_contain",[]):
        if word in output:
            tc_passed = False
            fail_reason.append(f"包含禁止词：{word}")

    if tc_passed:
        passed+=1
    else:
        failed+=1

    result.append({
        "id": tc["id"],
        "category": tc["category"],
        "prompt": tc["prompt"],
        "output": output,
        "passed":tc_passed,
        "fail_reason": fail_reason,
        "manusl_check": tc.get("manusl_check","")
    })
    print(f"{tc['id']}{'✅' if tc_passed else '❌'}")


# 生成HTML报告
total=len(result)
pass_rate=round(passed / total*100)

rows = ""
for r in result:
    status = "✅ PASS" if r["passed"] else "❌ FAIL"
    row_color = "#f0fff0" if r["passed"] else "#fff0f0"
    fail_info = "、".join(r["fail_reason"]) if r["fail_reason"] else ""
    manual = f"<br><small>⚠️ 需人工确认：{r['manusl_check']}</small>" if r["manusl_check"] else ""
    rows += f"""
    <tr style="background:{row_color}">
        <td>{r['id']}</td>
        <td>{r['category']}</td>
        <td>{r['prompt']}</td>
        <td style="max-width:400px;word-wrap:break-word">{r['output'][:200]}...</td>
        <td>{status}{manual}</td>
        <td style="color:red">{fail_info}</td>
    </tr>
    """

html = f"""
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>AI测试报告</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h1 {{ color: #333; }}
        .summary {{ display: flex; gap: 20px; margin: 20px 0; }}
        .card {{ padding: 20px; border-radius: 8px; text-align: center; min-width: 120px; }}
        .card-total {{ background: #e8f4fd; }}
        .card-pass {{ background: #f0fff0; }}
        .card-fail {{ background: #fff0f0; }}
        .card-rate {{ background: #fffbe6; }}
        .card h2 {{ margin: 0; font-size: 36px; }}
        .card p {{ margin: 4px 0 0; color: #666; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th {{ background: #4a90e2; color: white; padding: 10px; text-align: left; }}
        td {{ padding: 10px; border-bottom: 1px solid #ddd; vertical-align: top; }}
        .footer {{ margin-top: 30px; color: #999; font-size: 12px; }}
    </style>
</head>
<body>
    <h1>🤖 AI模型测试报告</h1>
    <p>测试模型：qwen-turbo &nbsp;|&nbsp; 测试时间：{datetime.now().strftime('%Y-%m-%d %H:%M')} &nbsp;|&nbsp; 测试场景：请假邮件 + 幻觉检测</p>
    
    <div class="summary">
        <div class="card card-total"><h2>{total}</h2><p>总用例数</p></div>
        <div class="card card-pass"><h2>{passed}</h2><p>通过</p></div>
        <div class="card card-fail"><h2>{failed}</h2><p>失败</p></div>
        <div class="card card-rate"><h2>{pass_rate}%</h2><p>通过率</p></div>
    </div>
    
    <table>
        <tr>
            <th>用例ID</th>
            <th>分类</th>
            <th>输入Prompt</th>
            <th>模型输出</th>
            <th>结果</th>
            <th>失败原因</th>
        </tr>
        {rows}
    </table>
    
    <div class="footer">
        <p>注：部分用例需结合人工判断，自动判断仅供参考。</p>
    </div>
</body>
</html>
"""

with open("test_report.html", "w", encoding="utf-8") as f:
    f.write(html)

print(f"\n✅ 报告已生成：test_report.html")
print(f"总计：{total}条 | 通过：{passed} | 失败：{failed} | 通过率：{pass_rate}%")
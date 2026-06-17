import dashscope
import os
import time
import statistics

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

def test_single_request(prompt):
    start_time = time.time()
    try:
        response = dashscope.Generation.call(
            model="qwen-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        end_time = time.time()
        output = response.output.text
        if output:
            return {
                "success": True,
                "response_time": round(end_time - start_time, 3),
                "output_length": len(output),
                "output": output[:50]
            }
        else:
            return {
                "success": False,
                "response_time": round(end_time - start_time, 3),
                "output_length": 0,
                "error": "输出为空"
            }
    except Exception as e:
        end_time = time.time()
        return {
            "success": False,
            "response_time": round(end_time - start_time, 3),
            "output_length": 0,
            "error": str(e)
        }

def run_performance_test(prompt, runs=5):
    print(f"\n测试场景：{prompt[:30]}...")
    print(f"执行次数：{runs}次")
    print("-" * 50)

    results = []
    success_count = 0

    for i in range(runs):
        result = test_single_request(prompt)
        results.append(result)
        if result["success"]:
            success_count += 1
            print(f"第{i+1:2d}次: {result['response_time']}秒 | 输出{result['output_length']}字符")
        else:
            print(f"第{i+1:2d}次: 失败({result['response_time']}秒) - {result.get('error', '未知')}")

    response_times = [r["response_time"] for r in results if r["success"]]

    print("\n【性能统计】")
    print(f"成功率: {success_count}/{runs} ({success_count/runs*100:.1f}%)")

    if response_times:
        avg = statistics.mean(response_times)
        print(f"平均响应时间: {avg:.3f}秒")
        print(f"最快/最慢: {min(response_times):.3f}秒 / {max(response_times):.3f}秒")
        if len(response_times) > 1:
            print(f"稳定性(标准差): {statistics.stdev(response_times):.3f}秒")
        print("✅ 平均响应时间达标(<3秒)" if avg < 3 else "❌ 平均响应时间超标(>3秒)")
        print("✅ 成功率达标(≥95%)" if success_count/runs >= 0.95 else "❌ 成功率不达标(<95%)")

    return {
        "prompt": prompt[:30],
        "runs": runs,
        "success_rate": success_count/runs,
        "avg_time": statistics.mean(response_times) if response_times else 0,
        "min_time": min(response_times) if response_times else 0,
        "max_time": max(response_times) if response_times else 0,
        "std_dev": statistics.stdev(response_times) if len(response_times) > 1 else 0
    }

scenarios = [
    "你好",
    "帮我写一封请假邮件",
    "请详细解释软件测试的完整流程，包括测试计划、测试设计、测试执行和测试报告各个阶段"
]

all_results = []
for scenario in scenarios:
    result = run_performance_test(scenario, runs=5)
    all_results.append(result)

with open("performance_report.txt", "w", encoding="utf-8") as f:
    f.write("LLM性能测试报告\n")
    f.write("=" * 50 + "\n")
    for r in all_results:
        f.write(f"\n场景: {r['prompt']}\n")
        f.write(f"成功率: {r['success_rate']*100:.1f}%\n")
        f.write(f"平均响应时间: {r['avg_time']:.3f}秒\n")
        f.write(f"最快/最慢: {r['min_time']:.3f}秒 / {r['max_time']:.3f}秒\n")
        f.write(f"稳定性(标准差): {r['std_dev']:.3f}秒\n")

print("\n已保存到 performance_report.txt")
from os import pread

import pandas as pd

# 模拟模型预测结果
# 1=垃圾邮件，0=正常邮件
data = {
    "id": list(range(1, 21)),
    "true_label": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    "pred_label": [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0],
    "confidence": [0.95,0.92,0.88,0.85,0.91,0.87,0.93,0.89,0.86,0.90,
                   0.83,0.78,0.82,0.79,0.84,0.45,0.38,0.42,0.51,0.48]
}

# 加入正常邮件
data["id"] += list(range(21, 101))
data["true_label"] += [0] * 80
data["pred_label"] += [0]*75 + [1]*5
data["confidence"] += [0.85]*75 + [0.72,0.68,0.71,0.69,0.73]

df = pd.DataFrame(data)

# 计算混淆矩阵四个值
TP = len(df[(df["true_label"] == 1) & (df["pred_label"] == 1)])
TN = len(df[(df["true_label"] == 0) & (df["pred_label"] == 0)])
FP = len(df[(df["true_label"] == 0) & (df["pred_label"] == 1)])
FN = len(df[(df["true_label"] == 1) & (df["pred_label"] == 0)])

print("="*50)
print("模型评估报告")
print("="*50)
print(f"\n混淆矩阵:")
print(f" TP(正确识别垃圾): {TP}")
print(f" TN(正确放行正常): {TN}")
print(f" FP(误杀正常邮件): {FP}")
print(f" FN(漏掉垃圾邮件): {FN}")

accuracy = (TP + TN) / (TP + TN + FP + FN)
precision = TP / (TP + FP) if (TP +FP) > 0 else 0
recall = TP / (TP + FN) if (TP + FN) > 0 else 0
f1 = 2 * precision * recall / (precision + recall) if precision + recall > 0 else 0

print(f"\n评估指标：")
print(f" 准确率 Accuracy: {accuracy:.2f}")
print(f" 精确率 Precision: {precision:.2f}")
print(f" 召回率 Recall: {recall:.2f}")
print(f" F1值 F1: {f1:.2f}")   

print(f"\n测试结论：")
print(f"\n测试结论:")
if recall < 0.8:
    print(f"  ❌ 召回率偏低({recall:.2%})，有较多垃圾邮件漏网，建议优化模型")
else:
    print(f"  ✅ 召回率达标({recall:.2%})")

if precision < 0.8:
    print(f"  ❌ 精确率偏低({precision:.2%})，误杀正常邮件较多，用户体验差")
else:
    print(f"  ✅ 精确率达标({precision:.2%})")

with open("metrics_report.txt", "w", encoding="utf-8") as f:
    f.write("模型评估报告\n")
    f.write("=" * 50 + "\n")
    f.write(f"准确率: {accuracy:.2%}\n")
    f.write(f"精确率: {precision:.2%}\n")
    f.write(f"召回率: {recall:.2%}\n")
    f.write(f"F1    : {f1:.2%}\n")

print("\n已保存到 metrics_report.txt")
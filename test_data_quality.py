import pandas as pd
import os

#模拟一份训练数据集
data = {
    "id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10],
    "text": [
        "这个产品很好用",
        "质量太差了",
        "还可以吧",
        None,
        "非常满意",
        "完全不推荐",
        "一般般",
        "超出预期",
        "",
        "物美价廉",
        "物美价廉"
    ],
    "label": [
        "正面",
        "负面",
        "中性",
        "正面",
        "正面",
        "负面",
        "中性",
        "正面",
        "中性",
        "正面",
        "正面"
    ],
    "confidence": [
        0.95,
        0.87,
        0.72,
        0.88,
        0.91,
        0.85,
        0.69,
        0.93,
        0.55,
        0.88,
        0.88
    ]
}

df = pd.DataFrame(data)

print("="*50)
print("数据质量检查报告:")
print("="*50)

issues = []

#1. 完整性检查
print(f"\n【1.完整性检查】")
null_count = df["text"].isnull().sum()
empty_count = (df["text"]=="").sum()
print(f"空值数量: {null_count}")
print(f"空字符串数量: {empty_count}")
if null_count > 0 or empty_count > 0:
    issues.append(f"完整性问题：{null_count}条空值， {empty_count}条空字符串")

#2. 唯一性检查
print(f"\n【2.唯一性检查】")
dup_ids = df["id"].duplicated().sum()
dup_texts = df["text"].dropna().duplicated().sum()
print(f"重复ID数量: {dup_ids}")
print(f"重复文本数量: {dup_texts}")
if dup_ids > 0:
    issues.append(f"唯一性问题：存在{dup_ids}条重复ID")
if dup_texts > 0:
    issues.append(f"唯一性问题：存在{dup_texts}条重复文本")

#3. 准确性检查
print(f"\n【3.准确性检查】")
valid_labels = ["正面","负面","中性"]
invalid_labels = df[~df["label"].isin(valid_labels)]["label"].tolist()
low_confidence = df[df["confidence"]< 0.7]
print(f"无效标签: {invalid_labels}")
print(f"低信度样本数量(<0.7): {len(low_confidence)}")
if len(invalid_labels) > 0:
    issues.append(f"准确性问题：{len(invalid_labels)}条无效标签")       
if len(low_confidence) > 0:
    issues.append(f"准确性问题：{len(low_confidence)}条低信度样本")

#4. 分布检查
print(f"\n【4.分布检查】")
label_dist = df["label"].value_counts(normalize=True)
print(f"标签分布:")
for label, ratio in label_dist.items():
    bar = "█" * int(ratio * 20)
    print(f"{label}:  {bar} {ratio*100:.1f}%")
max_ratio = label_dist.max()
if max_ratio < 0.6:
    issues.append(f"分布问题：最大类别占比{max_ratio*100:.1f}，存在数据不均衡")

#5. 汇总
print("\n" + "=" * 50)
print("问题汇总:")
if issues:
    for i, issue in enumerate(issues, 1):
        print(f"  {i}. ❌ {issue}")
else:
    print("  ✅ 未发现问题")

print(f"\n总计发现{len(issues)} 个数据质量问题")

# 保存报告
with open("data_quality_report_report.txt", "w", encoding="utf-8") as f:
    f.write("数据质量检查报告:\n")
    f.write("="*50 + "\n")
    for issue in issues:
        f.write(f"❌ {issue}\n")
    f.write(f"\n总计: {len(issues)} 个问题\n")

print("报告已保存至 data_quality_report_report.txt")

import dashscope
import os

dashscope.api_key = os.environ.get("DASHSCOPE_API_KEY")

def call_llm(prompt):
    response = dashscope.Generation.call(
        model="qwen-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.output.text

def test_generate_leave_email():
    output = call_llm("帮我写一封请假邮件")
    assert "请假" in output, "输出应包含'请假'"

def test_formal_tone():
    output = call_llm("请帮我写一封请假邮件，语气正式")
    assert len(output) > 50, "正式邮件输出不应过短"

def test_special_chars():
    output = call_llm("帮我写一封请假邮件 #$%@!")
    assert output is not None, "特殊字符输入不应导致空输出"

def test_reject_nonexistent_book():
    output = call_llm("软件测试领域有一本书叫《测试之魂》，作者是谁？")
    keywords = ["不存在", "没有", "未找到", "无法确认", "不确定"]
    has_rejection = any(k in output for k in keywords)
    assert has_rejection, "模型应该对不存在的书表示怀疑"

def test_answer_in_knowledge():
    knowledge = "公司年假制度:入职满1年享有5天年假，满3年10天"
    prompt = f"根据以下制度回答：{knowledge}\n\n问题：入职1年有几天年假？"
    output = call_llm(prompt)
    assert "5" in output, "应能从知识库中提取正确答案"

def test_reject_outside_knowledge():
    knowledge = "公司年假制度:入职满1年享有5天年假"
    prompt = f"根据以下制度回答：{knowledge}\n\n问题：产假有几天？"
    output = call_llm(prompt)
    rejection_words = ["未规定", "没有", "不包含", "未提及"]
    has_rejection = any(w in output for w in rejection_words)
    assert has_rejection, "知识库外的问题应被拒绝回答"
import json

def create_cn_prompt(x):
    format_type = x.get("Format", "")
    if format_type == "Multiple-choice":
        return "这是一道选择题。请仔细阅读问题，选择正确的答案。题目：" + \
               str(x["Question"]) + "\n以下哪个选项是正确的?选项:" + \
               '\n(A)' + str(x['A']) + '\n(B)' + str(x['B']) + '\n(C)' + str(x['C']) + '\n(D)' + str(x['D']) + \
               "\n请直接给出这个问题的答案(一个字母):"
    elif format_type == "Assertion":
        return "这是一个判断题。请确定以下题目是正确还是错误。题目：" \
               + str(x["Question"]) + "请直接给出答案(true or false):"
    elif format_type == "Fill-in-the-blank":
        return "这是一道填空题。请直接回答以下问题，无需解释或重复问题。问题：" \
               + str(x["Question"]) + "答案："
    elif format_type == "Open-ended":
        return "这是一道主观题：" \
               + str(x["Question"]) + "请简洁地回答这个问题："
    else:
        return "Format not recognized"
    
def create_en_prompt(x):
    format_type = x.get("Format", "")
    if format_type == "Multiple-choice":
        return  "This is a multiple-choice question. Please read the question carefully and choose the correct answer. Question:" + \
               str(x["Question"]) + "\nWhich one of the following options is correct? Options:" + \
               '\n(A)' + str(x['A']) + '\n(B)' + str(x['B']) + '\n(C)' + str(x['C']) + '\n(D)' + str(x['D']) + \
               "\nPlease provide the answer to this question directly (a single letter):" 
    elif format_type == "Assertion":
        return  "This is a true/false question. Please determine whether the following statement is true or false. Statement:" \
               + str(x["Question"]) + "Please give the answer directly (true or false):" 
    elif format_type == "Fill-in-the-blank":
        return  "You are a professor proficient in computer science. This is a fill-in-the-blank question. Give answers to the following question without explanation or repeating it.Question:" \
               + str(x["Question"]) + "Answer:" 
    elif format_type == "Open-ended":
        return  "This is a subjective question:" \
               + str(x["Question"]) + "Please provide a brief answer to this question:" 
    else:
        return "Format not recognized"


def process_jsonl_file(input_path,language):
    with open(input_path, 'r', encoding='utf-8') as file:
        for line in file:
            data = json.loads(line.strip())
            if language=="English":
                prompt = create_en_prompt(data)
            elif language=="Chinese":
                prompt = create_cn_prompt(data)
            else:
                raise
            print(prompt)

if __name__ == "__main__":
    process_jsonl_file('path_to_your_file.jsonl',language='English')
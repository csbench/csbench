import argparse
import json
import re
from test_call_llm import call_gpt

def score_json_object(json_obj, gen_with_gpt):
    answer = str(json_obj.get("Answer", "")).upper()
    output = json_obj.get("output", "")

    if json_obj["Format"] == "Multiple-choice":
        matches = re.findall(r'\b[ABCD]\b', output, re.IGNORECASE)
        json_obj["match"] = matches
        if matches:
            final_choice_str = matches[0].upper()
            json_obj["score"] = 1 if final_choice_str == answer else 0
        else:
            json_obj["score"] = 0
    elif json_obj["Format"] == "Assertion":
        match = re.search(r'\b(true|false)\b', output.lower())
        if match:
            final_choice_str = match.group(0)
            json_obj["score"] = 1 if final_choice_str == answer else 0
        else:
            json_obj["score"] = 0

    if gen_with_gpt and json_obj["Format"] in ["Fill-in-the-blank", "Open-ended"]:
        if json_obj["Format"] == "Fill-in-the-blank":
            question = json_obj['Question']
            correct_answer = json_obj['Answer']
            student_output = json_obj['output']
            language = json_obj['Language']
            prompt = create_fill_in_blank_prompt(question, correct_answer, student_output, language)
            
            try:
                gpt_response = call_gpt4(prompt)
            except json.decoder.JSONDecodeError:
                print(f"Error: Failed to parse JSON response for prompt: {prompt}")
                return None
            
            score = extract_fill_in_blank_score(gpt_response)
            json_obj['teacher_output'] = gpt_response
            json_obj['score'] = score

        elif json_obj["Format"] == "Open-ended":
            question = json_obj['Question']
            correct_answer = json_obj['Answer']
            student_output = json_obj['output']
            language = json_obj['Language']
            prompt = create_open_ended_prompt(question, correct_answer, student_output,language)
            
            try:
                gpt_response = call_gpt4(prompt)
            except json.decoder.JSONDecodeError:
                print(f"Error: Failed to parse JSON response for prompt: {prompt}")
                return None
            
            score = extract_open_ended_score(gpt_response)
            json_obj['teacher_output'] = gpt_response
            json_obj['score'] = score

    return json_obj

def create_fill_in_blank_prompt(question, correct_answer, student_output, language):
    if language == "English":
        return (f"You are now a teaching assistant. As a TA, your task is to grade the fill-in-the-blank assignments of computer science students."
                f"You will see the standard answer for each question (these answers are verified and completely correct), and you need to score the students' answers based on this."
                f"If the student's answer conveys the same meaning as the standard answer or other answers (different formats are also considered correct), then award 1 point; if not, then 0 points."
                f"Question: {question}\nStandard Answer: {correct_answer}\nStudent Response: {student_output}\n"
                f"Score (0 or 1):")
    elif language == "Chinese":
        return (f"你现在是一名助教。作为助教，你的任务是批改计算机专业学生的填空题作业。"
                f"你将会看到每个问题的标准答案（这些答案是经过验证的完全正确的），并需要基于此来评分学生的答案。"
                f"如果学生答案与标准答案或者其他答案表达含义相同（格式不同也算正确）即给1分，如果不同则0分"
                f"问题：{question}\n标准答案：{correct_answer}\n学生回答：{student_output}\n"
                f"评分（0或1）：")


def create_open_ended_prompt(question, correct_answer, student_output, language):
    if language == "English":
        return (f"You are now serving as a teaching assistant. In this role, your task is to grade the subjective homework assignments of computer science students. "
                f"You will be presented with the standard answers for each question (which are verified and completely correct), and you must use these to score the students' responses. "
                f"The grading scale ranges from 1 to 10 points, with 10 being the highest and 1 being the lowest. "
                f"When grading, please take into consideration the accuracy, relevance, completeness, and depth of thought of the answers. "
                f"Scores should be assigned based on the following *criteria*:\n\n"
                f"- **First Tier**: 1-3 points\n"
                f"  - **Accuracy**: The answer contains several fundamental errors, showing limited understanding.\n"
                f"  - **Relevance**: The answer has low relevance to the question and standard answer, with most content straying from the requirements.\n"
                f"  - **Completeness**: The answer omits multiple key points, failing to cover the main aspects of the question.\n\n"
                f"- **Second Tier**: 4-6 points\n"
                f"  - **Accuracy**: There are some errors in the answer, although most of the basic concepts are understood correctly.\n"
                f"  - **Relevance**: The answer is generally relevant to the question and standard answer, but some content does not fully conform to the requirements.\n"
                f"  - **Completeness**: The answer is fairly complete, but lacks some important details or certain key points are not fully elaborated.\n\n"
                f"- **Third Tier**: 7-8 points\n"
                f"  - **Accuracy**: The answer is almost entirely correct, with only very minor errors.\n"
                f"  - **Relevance**: The answer is highly relevant to the question and standard answer, focused and with almost no deviation from the topic.\n"
                f"  - **Completeness**: The answer is comprehensive and detailed, covering all key aspects very well.\n\n"
                f"- **Fourth Tier**: 9-10 points\n"
                f"  - **Accuracy**: The answer is free of any errors, demonstrating a deep understanding and precise grasp of the issue.\n"
                f"  - **Relevance**: The answer is in complete accordance with the requirements, strictly aligned with the question and standard answer, without any deviation.\n"
                f"  - **Completeness**: The answer is structured rigorously, logically organized, and systematically covers all aspects of the question.\n\n"
                f"**Grading Guide**: When assigning a score, please first make a preliminary assessment of accuracy based on the student's answer compared to the standard answer."
                f"Then, consider the relevance and completeness to determine the final score. "
                f"Ensure that each point awarded is based on a fair and justified comprehensive evaluation.\n"
                f"Question: {question}\nStandard Answer: {correct_answer}\nStudent Answer: {student_output}\n"
                f"Score (1-10):")
    elif language == "Chinese":
        return (f"你现在是一名助教。作为助教，你的任务是批改计算机专业学生的主观题作业。"
                f"你将会看到每个问题的标准答案（这些答案是经过验证的完全正确的），并需要基于此来评分学生的答案。"
                f"评分的范围是1-10分，其中10分为最高分，1分为最低分。在评分时，请综合考虑答案的正确性、相关性、完整性以及思考的深度。"
                f"你需要按照以下*标准*给出分数：\n\n"
                f"- **第一档：1-3分**\n"
                f"  - **正确性**：答案中包含多个基本概念的错误，显示出有限的理解。\n"
                f"  - **相关性**：答案与问题和标准答案的相关性很低，大部分内容偏离题目要求。\n"
                f"  - **完整性**：答案遗漏多个关键点，未能覆盖问题的主要方面。\n\n"
                f"- **第二档：4-6分**\n"
                f"  - **正确性**：答案中存在一些错误，尽管大部分基本概念理解正确。\n"
                f"  - **相关性**：答案基本上与问题和标准答案相关，但有一些内容不完全贴合题目要求。\n"
                f"  - **完整性**：答案较为完整，但缺失一些重要细节或某些关键点未充分阐述。\n\n"
                f"- **第三档：7-8分**\n"
                f"  - **正确性**：答案几乎完全正确，只有极少数小错误。\n"
                f"  - **相关性**：答案与问题和标准答案高度相关，专注并且几乎无偏离主题。\n"
                f"  - **完整性**：答案内容全面且详尽，很好地覆盖了所有关键方面。\n\n"
                f"- **第四档：9-10分**\n"
                f"  - **正确性**：答案无任何错误，展现了对问题深刻理解和精确掌握。\n"
                f"  - **相关性**：答案完全符合题目要求，严格对齐问题和标准答案，无任何偏离。\n"
                f"  - **完整性**：答案结构严谨，条理清晰，全面而系统地覆盖了问题的所有方面。\n\n"
                f"**评分指南：**在给出评分时，请首先依据学生答案与标准答案进行正确性的初步评估。"
                f"随后综合考虑答案的相关性、完整性来确定最终分数。"
                f"请确保每一分的给出都是基于公正和有据可依的综合评估。"
                f"问题：{question}\n标准答案：{correct_answer}\n学生回答：{student_output}\n"
                f"评分（1-10）：")


def extract_fill_in_blank_score(gpt_output):
    if not isinstance(gpt_output, str):
        gpt_output = str(gpt_output)
    matches = re.findall(r'\b(0|1)\b', gpt_output)
    return int(matches[0]) if matches else 0

def extract_open_ended_score(gpt_output):
    if not isinstance(gpt_output, str):
        gpt_output = str(gpt_output)
    matches = re.findall(r'\b([1-9]|10)\b', gpt_output)
    return int(matches[0]) / 10 if matches else 0

def main():
    parser = argparse.ArgumentParser(description="Process JSON files for grading.")
    parser.add_argument("--judge_with_gpt", type=int, choices=[0, 1], default=0,
                        help="Generate scores using GPT for all formats if 1, else only for MCQ and Assertion")
    parser.add_argument("input_file_path", type=str, help="Path to the input JSON file.")
    args = parser.parse_args()

    output_file_path = args.input_file_path  # Overwrite the same file

    processed_lines = []
    with open(args.input_file_path, "r", encoding="utf-8") as file:
        for line in file:
            json_obj = json.loads(line.strip())
            processed_json = score_json_object(json_obj, args.judge_with_gpt)
            processed_lines.append(json.dumps(processed_json, ensure_ascii=False))

    with open(output_file_path, "w", encoding="utf-8") as file:
        for line in processed_lines:
            file.write(f"{line}\n")

if __name__ == "__main__":
    main()
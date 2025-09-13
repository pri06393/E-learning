from fastapi import FastAPI, HTTPException
import json

def check_question(question_string):

    question_object = json.loads(question_string)

    if question_object["content"].strip() == "":
        # return print(f'Question content cannot be an empty string')
        raise HTTPException(status_code=404, detail="question_content not given")
        
    if len(question_object["options"]) < 2:
        # return print(f'Need atleast 2 options')
        raise HTTPException(status_code=404, detail="need atleast 2 options")
    print("hello")
    return question_string

def check_answer(answer_string, question_string):

    answer_object = json.loads(answer_string)
    question_object = json.loads(question_string)

    if len(answer_object) == 0:
        # return print("answer_set should not be empty")
        raise HTTPException(status_code=404, detail="answer_set should not be empty")
    if len(answer_object)>len(question_object["options"]):
        # return print("answer_set should not have more options then questions")
        raise HTTPException(status_code=404, detail="nswer_set should not have more options then questions")

    return answer_object

# def check_answer_set(result_string, question_ids):

#     result_object = json.loads(result_string)
#     answer_set = dict(zip(question_ids, result_object))

#     return answer_set

#     # print("content:",question_object["content"])
#     # print("options:",question_object["options"])

def check_answer_set(result_string, question_ids):
    # Parse JSON string (user answers dictionary)
    result_object = json.loads(result_string)

    # Convert keys to int (since JSON keys are always strings)
    answer_set = {int(k): v for k, v in result_object.items()}

    # Optional: validate that only known question_ids are present
    for qid in answer_set.keys():
        if qid not in question_ids:
            raise HTTPException(status_code=400, detail=f"Invalid question id {qid}")

    return answer_set
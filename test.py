import json
import random
import time

def load_question():
    with open("question.json","r",encoding="UTF-8") as file:
        return json.load(file)
    
def ask_question(question):
    print("\n"+question["題目"])
    for i, option in enumerate(question["選項"],start=1):
        print(f"{i}. {option}")

    answer=input("請輸入選項號碼:")

    try:
        selected_option=int(answer)-1
        if question["選項"][selected_option]==question["答案"]:
            return True
    except (ValueError,IndexError):
        pass

    return False
    
def start_quiz():
    question=load_question()
    category=input(f"選擇題目類型 {list(question.keys())}:")

    if category not in question:
        print("類別不存在!")
        return
    selected_question=random.sample(question[category],min(5,len(question[category])))
    score=0

    for question in selected_question:
        if ask_question(question):
            score +=20
            print("答對了!")
        else:
            print(f"錯了，正確答案是:{question['答案']}")

    print(f"\n測驗結束!您的得分:{score}")

if __name__=="__main__":
    start_quiz()
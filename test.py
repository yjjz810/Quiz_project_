import json
import random
import threading
import time

def countdown(seconds, stop_event):
    for i in range(seconds, 0, -1):
        if stop_event.is_set():
            return
        print(f"\r剩下 {i} 秒...：請輸入選項號碼：", end="", flush=True)
        time.sleep(1)
    if not stop_event.is_set():
        print("\r時間到！                         ")  # 清除舊字，讓畫面乾淨
        stop_event.set()

def timed_input(timeout):
    result = [None]
    stop_event = threading.Event()

    def read_input():
        try:
            result[0] = input()  # 這行配合上面的 print，會在同一行輸入
        except:
            pass
        finally:
            stop_event.set()

    input_thread = threading.Thread(target=read_input)
    input_thread.daemon = True
    input_thread.start()

    countdown_thread = threading.Thread(target=countdown, args=(timeout, stop_event))
    countdown_thread.start()

    input_thread.join(timeout)
    stop_event.set()
    countdown_thread.join()

    return result[0]

def load_question():
    with open("question.json", "r", encoding="UTF-8") as f:
        return json.load(f)

def ask_question(question):
    print("\n" + question["題目"])
    for i, option in enumerate(question["選項"], 1):
        print(f"{i}. {option}")

    answer = timed_input(10)

    if answer is None:
        print("你沒有作答，本題跳過！")
        return False

    try:
        selected = int(answer) - 1
        if question["選項"][selected] == question["答案"]:
            return True
    except (ValueError, IndexError):
        pass

    return False

def start_quiz():
    data = load_question()
    category = input(f"選擇題目類型 {list(data.keys())}：")

    if category not in data:
        print("沒有這個類型喔")
        return

    questions = random.sample(data[category], min(5, len(data[category])))
    score = 0

    for q in questions:
        if ask_question(q):
            print("答對了！")
            score += 20
        else:
            print(f"錯了，正確答案是：{q['答案']}")

    print(f"\n測驗結束，你的總得分是：{score}")

if __name__ == "__main__":
    start_quiz()
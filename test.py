import json
import random
import threading #用來進行多現成操作，讓計時和輸入同時進行
import time #設置延遲和倒數計時
from inputimeout import inputimeout, TimeoutOccurred

def countdown(timeout, stop_event):
    for i in range(timeout, 0, -1):
        if stop_event.is_set():
            return
        print(f"\r剩下 {i} 秒，請輸入選項號碼：", end="", flush=True)
        time.sleep(1) #每一秒鐘等待一次
    if not stop_event.is_set():
        stop_event.set() #最後當倒數結束且 stop_event 沒有被設定時，會觸發 stop_event.set()，並打印 時間到！
        print("\n時間到！")

def timed_input(timeout):
    result = [None]
    stop_event = threading.Event()

    def read_input():
        try:
            user_input = inputimeout(prompt=f"剩下 {timeout} 秒，請輸入選項號碼：", timeout=timeout)
            if not stop_event.is_set():
                result[0] = user_input
        except TimeoutOccurred:
            pass
        finally:
            stop_event.set()

    input_thread = threading.Thread(target=read_input) #建立新的線程來執行read_input函數，讓input()不會堵塞計時
    countdown_thread = threading.Thread(target=countdown, args=(timeout, stop_event)) #建立新的線程來執行countdown函數

    input_thread.start() 
    countdown_thread.start() #這兩行啟動兩個現成，讓倒數和輸入可以併行進行

    input_thread.join(timeout) #等待input_thread完成，並設定超時時間。如果使用者在超時時間內沒有輸入，input_thread會自動結束
    stop_event.set()
    countdown_thread.join()

    return result[0]

def load_question():
    with open("question.json", "r", encoding="utf-8") as f: #讀取json，指定檔案編碼方式為utf-8，以便正確處理中文字符
        return json.load(f)

def ask_question(q): #q是一個字典，包含了題目的詳細資訊
    print("\n" + q["題目"])
    for i, opt in enumerate(q["選項"], 1):
        print(f"{i}. {opt}")

    ans = timed_input(10)

    if ans is None: #如果沒有輸入會跳過這題
        print("你沒有作答，本題跳過！")
        return False

    try:                                    #用來處理錯誤，如果使用者輸入無效選項會跳過這題
        selected = int(ans.strip()) - 1
        if 0 <= selected < len(q["選項"]) and q["選項"][selected] == q["答案"]: #len是用來計算東西的長度或個數，這行的意思是輸入有效的選項編號，(、1、2、3、4)
            return True
    except:
        pass

    return False

def start_quiz():
    data = load_question()
    category = input(f"選擇題目類型 {list(data.keys())}：") #提示使用者選擇題型，並列出可選題目類型

    if category not in data:
        print("沒有這個類型喔")
        return

    questions = random.sample(data[category], min(5, len(data[category]))) #從選擇題型中隨機挑選五題
    score = 0 #初始化分數為0

    for q in questions: #對每一題進行處理，並根據答案是否正確更新分數
        if ask_question(q):
            print("答對了！")
            score += 20
        else:
            print(f"錯了，正確答案是：{q['答案']}")

    print(f"\n測驗結束，你的總得分是：{score}")

if __name__ == "__main__":
    start_quiz()
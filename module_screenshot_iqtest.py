import json
import os
import time

import cv2
import keyboard
import numpy as np
import pandas as pd
import pyautogui
import pytesseract
from addict import Dict


def check_esc():
    if keyboard.is_pressed("esc"):
        print("偵測到 ESC 按鍵，程式結束...")
        return True
    return False


def run():
    # 倒數
    foo = 5
    while foo:
        print(f"倒數 {foo}...")
        time.sleep(1)
        foo -= 1
        if check_esc():
            return None

    # 初始化
    config = {
        "dir_path": os.path.join(os.getcwd(), "iqtest"),
        "filenames": ["answer_area.png", "end.png"],
        "mouse": {
            "A": {"x": 408, "y": 374},
            "B": {"x": 408, "y": 420},
            "C": {"x": 408, "y": 468},
            "D": {"x": 408, "y": 528},
            "V": {"x": 490, "y": 634},
            "X": {"x": 766, "y": 634},
        },
        "region": {
            "answer_area": (436, 604, 399, 68),
            "q": (290, 180, 720, 158),
            "qa": (290, 145, 716, 560),
            "response": (297, 144, 132, 35),
        },
        "pixel": ["2560x1600", "1920x1080"],
    }

    # 根據當前螢幕解析度，選擇對應的資料夾
    screen_width, screen_height = pyautogui.size()
    pixel = f"{screen_width}x{screen_height}"
    if pixel not in config["pixel"]:
        print(f"當前解析度為 {pixel}，僅允許 {config['pixel']}!")
        return None
    else:
        for idx, filename in enumerate(config["filenames"]):
            name, extension = os.path.splitext(filename)
            if extension != ".txt":
                config["filenames"][idx] = f"{name}_{pixel}{extension}"

    # 確認必要檔案存在於指定路徑
    for filename in config["filenames"]:
        file_path = os.path.join(config["dir_path"], filename)
        if not os.path.exists(file_path):
            print(f"找不到 {file_path} !")
            return None
        if check_esc():
            return None
    print(f'必要檔案 {config["filenames"]} 均存在...')

    # 刪除暫存檔
    if f"iqtest_tmp_{pixel}.png" in os.listdir(config["dir_path"]):
        file_path = os.path.join(config["dir_path"], f"iqtest_tmp_{pixel}.png")
        os.remove(file_path)

    # 更新 ct
    ct = 0
    for filename in os.listdir(config["dir_path"]):
        if filename.startswith("iqtest_q_"):
            foo = int(filename.split("_")[2])
            if foo > ct:
                ct = foo
    ct += 1

    # 讀檔
    file_path = os.path.join(config["dir_path"], "sample.json")
    if not os.path.exists(file_path):
        table = Dict()
    else:
        table = pd.read_json(file_path)
        table = Dict(table.to_dict())

    # 截圖
    while True:
        try:
            # 目前頁面: 作答階段
            file_path = os.path.join(config["dir_path"], f"answer_area_{pixel}.png")
            pyautogui.locateOnScreen(file_path, region=config["region"]["answer_area"])

            # 目前顯示的是新題目
            new_q = False
            if f"iqtest_tmp_{pixel}.png" not in os.listdir(config["dir_path"]):
                new_q = True
            else:
                try:
                    file_path = os.path.join(
                        config["dir_path"], f"iqtest_tmp_{pixel}.png"
                    )
                    pyautogui.locateOnScreen(file_path, region=config["region"]["q"])
                except pyautogui.ImageNotFoundException:
                    new_q = True
                    print("題目還沒刷新!")

            # 目前顯示的是新題目
            if new_q:
                # 目前頁面: 結束階段
                try:
                    file_path = os.path.join(config["dir_path"], f"end_{pixel}.png")
                    pyautogui.locateOnScreen(file_path, region=config["region"]["q"])
                    print("活動結束...")

                    file_path = os.path.join(config["dir_path"], "sample.json")
                    with open(file_path, "w", encoding="utf-8") as fp:
                        json.dump(table, fp, ensure_ascii=False, indent=4)
                    return None
                except pyautogui.ImageNotFoundException:
                    # 截圖(題目+選項)
                    filename = f"iqtest_qa_{str(ct).zfill(4)}_{pixel}.png"  # 檔名
                    img = pyautogui.screenshot(
                        region=config["region"]["qa"]
                    )  # 題目和選項
                    img.save(os.path.join(config["dir_path"], filename))  # 路徑

                    # 截圖(僅題目)
                    filename = f"iqtest_q_{str(ct).zfill(4)}_{pixel}.png"  # 檔名
                    img = pyautogui.screenshot(region=config["region"]["q"])  # 只有題目
                    img.save(os.path.join(config["dir_path"], filename))  # 路徑
                    print(f"取得題目 {filename}...")
                    filename = f"iqtest_tmp_{pixel}.png"  # 檔名
                    img.save(os.path.join(config["dir_path"], filename))  # 路徑

                    # 將與目標顏色不同的像素設為白色
                    file_path = os.path.join(config["dir_path"], filename)
                    img = cv2.imread(file_path)
                    target_color = [120] * 3
                    mask = np.any(img >= target_color, axis=-1)
                    img[mask] = [255, 255, 255]

                    # 使用 pytesseract 來辨識文字
                    question = pytesseract.image_to_string(
                        img, lang="chi_tra+chi_sim+eng"
                    )
                    question = question.replace(" ", "").replace("\n", "")

                    if not table[question]:
                        table[question] = {"A": "?", "B": "?", "C": "?", "D": "?"}

                    not_sure = ""
                    is_correct = ""
                    for k, v in table[question].items():
                        if v == "V":
                            is_correct = k
                        elif v == "?":
                            not_sure = k

                    if is_correct:
                        pyautogui.moveTo(
                            config["mouse"][is_correct]["x"],
                            config["mouse"][is_correct]["y"],
                        )
                    elif not_sure:
                        pyautogui.moveTo(
                            config["mouse"][not_sure]["x"],
                            config["mouse"][not_sure]["y"],
                        )
                    pyautogui.mouseDown()
                    time.sleep(0.25)

                    # 點擊 [V]
                    pyautogui.moveTo(
                        config["mouse"]["V"]["x"], config["mouse"]["V"]["y"]
                    )
                    pyautogui.mouseDown()
                    time.sleep(1.5)

                    if not is_correct:
                        # 截圖(回饋)
                        filename = "response.png"  # 檔名
                        img = pyautogui.screenshot(region=config["region"]["response"])
                        img.save(os.path.join(config["dir_path"], filename))  # 路徑
                        img.save(
                            os.path.join(
                                config["dir_path"],
                                f"iqtest_response_{str(ct).zfill(4)}_{pixel}.png",
                            )
                        )  # 路徑

                        # 將與目標顏色不同的像素設為白色
                        file_path = os.path.join(config["dir_path"], filename)
                        img = cv2.imread(file_path)
                        target_color = [190] * 3
                        mask = np.any(img <= target_color, axis=-1)
                        img[mask] = [0, 0, 0]

                        # 使用 pytesseract 來辨識文字
                        response = pytesseract.image_to_string(
                            img, lang="chi_tra+chi_sim+eng"
                        )
                        response = response.replace(" ", "").replace("\n", "")

                        if response == "答對了":
                            table[question][not_sure] = "V"
                        elif response in ["答錯了", "化妳"]:
                            table[question][not_sure] = "X"
                        else:
                            print("無法辨識回饋!")

                    # 更新
                    ct += 1
        except pyautogui.ImageNotFoundException:
            print("沒看到題目!")


if __name__ == "__main__":
    # 需要系統管理員權限開啟程式(ide or cmd)，才能使 pyautogui 正常執行
    run()

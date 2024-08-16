import json
import os

import cv2
import pandas as pd
import pytesseract


def run():
    # 初始化
    config = {
        "dir_path": os.path.join(os.getcwd(), "iqtest"),
    }

    if "sample.json" in os.listdir(config["dir_path"]):
        file_path = os.path.join(config["dir_path"], "sample.json")
        output = pd.read_json(file_path).to_dict()
    else:
        output = dict()

    for filename in os.listdir(config["dir_path"]):
        if filename.startswith("iqtest_q_"):
            file_path = os.path.join(config["dir_path"], filename)
            img = cv2.imread(file_path, cv2.IMREAD_UNCHANGED)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)  # BGRA
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 灰階

            # 取得圖片高度、寬度
            h = img.shape[0]
            w = img.shape[1]

            # 依序取出圖片中每個像素
            for x in range(w):
                for y in range(h):
                    if gray[y, x] > 120:
                        img[y, x, 3] = 0

            # 使用 pytesseract 來辨識文字
            text = pytesseract.image_to_string(img, lang="chi_tra+chi_sim+eng")

            # 打印識別的文字
            if text in output.keys():
                print(f"題目重複: {filename} <-> {output[text]['filename']}!")
            else:
                output[text] = {"ans": "", "filename": filename}
                print(f"找到新題目: {filename}...")

    file_path = os.path.join(config["dir_path"], "sample.json")
    with open(file_path, "w", encoding="utf-8") as fp:
        json.dump(output, fp, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    # 需要系統管理員權限開啟程式(ide or cmd)，才能使 pyautogui 正常執行
    run()

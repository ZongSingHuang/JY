import os
import time

import keyboard
import pyautogui
from skimage.metrics import structural_similarity as ssim


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
        "filenames": ["answer_area.png"],
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
        },
        "pixel": ["2560x1600"],
    }

    # 根據當前螢幕解析度，選擇對應的資料夾
    screen_width, screen_height = pyautogui.size()
    pixel = f"{screen_width}x{screen_height}"
    if pixel not in config["pixel"]:
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
    # 暫時不需要

    # 截圖
    while True:
        try:
            # 確認目前頁面包含作答區
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

            # 目前顯示的是新題目
            if new_q:
                # 是否曾見過這題
                had_seem = False
                for filename in os.listdir(config["dir_path"]):
                    if filename.startswith("iqtest_q_"):
                        try:
                            file_path = os.path.join(config["dir_path"], filename)
                            pyautogui.locateOnScreen(
                                file_path, region=config["region"]["q"]
                            )
                            had_seem = True
                            break
                        except pyautogui.ImageNotFoundException:
                            had_seem = False

                if not had_seem:
                    # 截圖(僅題目)
                    filename = f"iqtest_q_{str(ct).zfill(3)}_{pixel}.png"  # 檔名
                    im = pyautogui.screenshot(region=config["region"]["q"])  # 只有題目
                    im.save(os.path.join(config["dir_path"], filename))  # 路徑
                    print(f"取得新題目 {filename}...")
                    filename = f"iqtest_tmp_{pixel}.png"  # 檔名
                    im.save(os.path.join(config["dir_path"], filename))  # 路徑

                    # 截圖(題目+選項)
                    filename = f"iqtest_qa_{str(ct).zfill(3)}_{pixel}.png"  # 檔名
                    im = pyautogui.screenshot(
                        region=config["region"]["qa"]
                    )  # 題目和選項
                    im.save(os.path.join(config["dir_path"], filename))  # 路徑

                    # 點擊 [V]
                    pyautogui.moveTo(
                        config["mouse"]["V"]["x"], config["mouse"]["V"]["y"]
                    )
                    pyautogui.mouseDown()
                    pyautogui.mouseUp()
                    time.sleep(1)

                    # 更新
                    ct += 1
        except pyautogui.ImageNotFoundException:
            111


if __name__ == "__main__":
    # 需要系統管理員權限開啟程式(ide or cmd)，才能使 pyautogui 正常執行
    run()

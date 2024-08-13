import os
import time

import keyboard
import pyautogui


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
        "dir_path": os.path.join(os.getcwd(), "giftcode"),
        "filenames": ["giftcode.txt", "panel.png", "topup.png", "already.png"],
        "mouse": {"panel": {"x": 318, "y": 815}, "already": {"x": 599, "y": 512}},
        "region": {
            "panel": (248, 780, 98, 56),
            "topup": (208, 173, 510, 490),
            "already": (471, 355, 265, 186),
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

    # 讀檔
    file_path = os.path.join(config["dir_path"], "giftcode.txt")
    with open(file_path, "r") as file:
        content = file.read()
    giftcodes = [(v.split()[0], v.split()[1]) for v in content.split("\n")]
    if not len(giftcodes):
        print(f"{file_path} 裡，沒有直播碼!")
        return None
    else:
        print(f"{file_path} 裡，有 {len(giftcodes)} 個直播碼...")

    # [儲值點數] 有擺在 [快捷列 3]-[第 1 個快捷鍵]
    try:
        file_path = os.path.join(config["dir_path"], f"panel_{pixel}.png")
        pyautogui.locateOnScreen(file_path, region=config["region"]["panel"])
    except pyautogui.ImageNotFoundException:
        print(111)
        return None

    # 儲值直播碼
    sucess_ct = 0
    fail_ct = 0
    for idx, (sn, pwd) in enumerate(giftcodes):
        if check_esc():
            return None

        # 點擊 [快捷列 3]-[第 1 個快捷鍵]-[儲值點數]
        pyautogui.moveTo(config["mouse"]["panel"]["x"], config["mouse"]["panel"]["y"])
        pyautogui.mouseDown()
        pyautogui.mouseUp()
        time.sleep(1)

        # 確認畫面已經切換到 [設定儲值點數]
        try:
            file_path = os.path.join(config["dir_path"], f"topup_{pixel}.png")
            pyautogui.locateOnScreen(file_path, region=config["region"]["topup"])
        except pyautogui.ImageNotFoundException:
            print(222)
            return None

        # 輸入直播碼
        for v in sn:
            pyautogui.press(v)  # 輸入序號
            if check_esc():
                return None
        pyautogui.press("enter")  # 換行(enter)
        for v in pwd:
            pyautogui.press(v)  # 輸入密碼
            if check_esc():
                return None
        pyautogui.press("enter")  # 執行(enter)
        time.sleep(1)

        # 自動關閉【卡已用過】的彈跳視窗
        try:
            file_path = os.path.join(config["dir_path"], f"already_{pixel}.png")
            pyautogui.locateOnScreen(file_path, region=config["region"]["already"])
            fail_ct += 1
            print(f"第 {idx + 1} 個直播碼，重複輸入!")
            pyautogui.moveTo(
                config["mouse"]["already"]["x"], config["mouse"]["already"]["y"]
            )
            pyautogui.mouseDown()
            pyautogui.mouseUp()
            time.sleep(1)
        except Exception:
            sucess_ct += 1
            print(f"第 {idx + 1} 個直播碼，成功執行...")
    print(f"總共有 {len(giftcodes)} 個直播碼，成功 {sucess_ct} 次；失敗 {fail_ct} 次")


if __name__ == "__main__":
    # 需要系統管理員權限開啟程式(ide or cmd)，才能使 pyautogui 正常執行
    run()

import msvcrt
import os
import subprocess
import time

import pyautogui


def script_gift_code():
    def auto_enter_gift_code():
        # 提示
        print("執行直播碼自動輸入環節...")

        # 讀取筆記本內的直播碼
        gift_codes_path = os.path.join(os.getcwd(), "直播碼.txt")
        if not os.path.isfile(gift_codes_path):
            print(f"找不到 {gift_codes_path} !")
            return None
        with open(gift_codes_path, "r") as file:
            content = file.read()
        gift_codes = [(v.split()[0], v.split()[1]) for v in content.split("\n")]
        print(f"{gift_codes_path} 裡，紀載了 {len(gift_codes)} 個直播碼")

        # 掃視
        sucess_ct = 0
        fail_ct = 0
        for idx, (sn, pwd) in enumerate(gift_codes):
            # 強制中止
            print("正在輸入直播碼，直接關閉程式可以中止...")
            # 按下遊戲中，快捷列的 f1(儲值點數)
            pyautogui.keyDown("f1")
            pyautogui.keyUp("f1")
            # 輸入序號
            for v in sn:
                pyautogui.press(v)
            time.sleep(1)
            # 換行(enter)
            pyautogui.press("enter")
            # 輸入密碼
            for v in pwd:
                pyautogui.press(v)
            time.sleep(1)
            # 執行(enter)
            pyautogui.press("enter")
            time.sleep(1)
            # 自動關閉【卡已用過】的彈跳視窗
            try:
                # 用 pyautogui.click() 會發生第一次執行時不會成功讓滑鼠左鍵點擊，所以改用 moveTo + mouseDown + mouseUp
                fail_ct += 1
                is_register = pyautogui.locateOnScreen(
                    "sample01.png"
                )  # 比對當前視窗截圖與 sample 是否有一樣的
                ok_pt_x, ok_pt_y = pyautogui.center(
                    is_register
                )  # 如果有，就取得視窗中，符合 sample 的中心位置
                time.sleep(1)
                pyautogui.moveTo(ok_pt_x, ok_pt_y + 40)  # 移動滑鼠
                time.sleep(1)
                pyautogui.mouseDown()  # 點擊滑鼠左鍵
                pyautogui.mouseUp()
                print(f"第 {idx + 1} 個直播碼，重複輸入!")
            except Exception:
                sucess_ct += 1
                print(f"第 {idx + 1} 個直播碼，成功執行...")
            time.sleep(1)
        print(
            f"總共有 {len(gift_codes)} 個直播碼，成功 {sucess_ct} 次；失敗 {fail_ct} 次"
        )

    while True:
        print("是否已經把【指令】-【雜項】-【儲值點數】拖移到快捷列的第 1 個位置(F1)?")
        print("1. 確定!")
        print("2. 怎麼拖移?")
        print("3. 怎麼確定有拖移到正確位置?")
        print("4. 回到主選單")
        choice = msvcrt.getch()
        match choice:
            case b"1":
                for i in range(5, 0, -1):
                    print(f"{i} 秒後執行，請趕緊用滑鼠左鍵點點擊 1 下遊戲畫面!")
                    time.sleep(1)
                auto_enter_gift_code()
            case b"2" | b"3":
                manual_gift_code_path = os.path.join(os.getcwd(), "儲存點數.png")
                subprocess.Popen(["start", "", manual_gift_code_path], shell=True)
            case b"4":
                break
            case _:
                print("指令錯誤!。")


def script_training_mana():
    def auto_training_mana():
        # 提示
        print("執行修練內力環節...")
        while True:
            # 按下遊戲中，快捷列的 f4(修練內力)
            pyautogui.keyDown("f4")
            pyautogui.keyUp("f4")
            # 強制中止
            print("正在修練內力，，直接關閉程式可以中止...")
            time.sleep(1)

    while True:
        print("是否已經把【指令】-【武學】-【修練內力】拖移到快捷列的第 4 個位置(F4)?")
        print("1. 確定!")
        print("2. 怎麼拖移?")
        print("3. 怎麼確定有拖移到正確位置?")
        print("4. 回到主選單")
        choice = msvcrt.getch()
        match choice:
            case b"1":
                for i in range(5, 0, -1):
                    print(f"{i} 秒後執行，請趕緊用滑鼠左鍵點點擊 1 下遊戲畫面!")
                    time.sleep(1)
                auto_training_mana()
            case b"2" | b"3":
                manual_mana_path = os.path.join(os.getcwd(), "修練內力.png")
                subprocess.Popen(["start", "", manual_mana_path], shell=True)
            case b"4":
                break
            case _:
                print("指令錯誤!。")


def main():
    # 檢查必要檔案是否存在
    everything_can_found = True
    gift_codes_path = os.path.join(os.getcwd(), "直播碼.txt")
    if not os.path.isfile(gift_codes_path):
        print(f"找不到 {gift_codes_path} !")
        everything_can_found = False
    sample_path = os.path.join(os.getcwd(), "sample01.png")
    if not os.path.isfile(sample_path):
        print(f"找不到 {sample_path} !")
        everything_can_found = False
    manual_mana_path = os.path.join(os.getcwd(), "修練內力.png")
    if not os.path.isfile(manual_mana_path):
        print(f"找不到 {manual_mana_path} !")
        everything_can_found = False
    manual_gift_code_path = os.path.join(os.getcwd(), "儲存點數.png")
    if not os.path.isfile(manual_gift_code_path):
        print(f"找不到 {manual_gift_code_path} !")
        everything_can_found = False
    manual_admin_path = os.path.join(os.getcwd(), "系統管理員.png")
    if not os.path.isfile(manual_admin_path):
        print(f"找不到 {manual_admin_path} !")
        everything_can_found = False

    if not everything_can_found:
        os.system("pause")
    else:
        print("是否已經以系統管理員身份開啟本程式?")
        print("1. 確定!")
        print("2. 什麼是系統管理員?")
        print("3. 如何用系統管理員身份打開程式?")
        print("Esc. 退出程式")
        choice = msvcrt.getch()
        match choice:
            case b"1":
                while True:
                    print("請按下要執行的功能：")
                    print("1. 直播碼")
                    print("2. 修練內力")
                    print("Esc. 退出程式")

                    choice = msvcrt.getch()
                    match choice:
                        case b"1":
                            script_gift_code()
                        case b"2":
                            script_training_mana()
                        case b"\x1b":
                            print("結束程式!。")
                            break
                        case _:
                            print("指令錯誤!。")
            case b"2" | b"3":
                manual_admin_path = os.path.join(os.getcwd(), "系統管理員.png")
                subprocess.Popen(["start", "", manual_admin_path], shell=True)
            case b"4":
                os.system("pause")
            case _:
                print("指令錯誤!。")
        os.system("pause")


if __name__ == "__main__":
    # 需要系統管理員權限開啟程式(ide or cmd)，才能使 pyautogui 正常執行
    main()

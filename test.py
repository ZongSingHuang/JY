import os
import time

import pyautogui

# 初始化
title = "2560x1600_iqtest"  # 標題
orign_path = os.path.join(os.getcwd(), "2560x1600", "iqtest")  # 路徑

# 計數器
if not os.listdir(orign_path):
    ct = 0
else:
    ct = int(sorted(os.listdir(orign_path))[-1].split("_")[2])

foo = 5
while foo:
    print(f"倒數 {foo}...")
    time.sleep(1)
    foo -= 1

while True:
    # 確認目前正在進行答題
    # 擷取畫面
    im_q = pyautogui.screenshot(region=(290, 173, 716, 158))  # 只有題目
    im_qa = pyautogui.screenshot(region=(290, 145, 716, 560))  # 題目和選項

    # 比對暫存檔
    # 確認暫存檔存在
    # 暫存檔與當前截圖相同
    # 暫存檔與當前截圖不符合

    # 存檔
    filename_q = f"{title}_{str(ct).zfill(3)}_q.png"  # 檔名
    im_q.save(os.path.join(orign_path, filename_q))  # 路徑
    print(f"{filename_q} 儲存完成")  # 打印
    filename_qa = f"{title}_{str(ct).zfill(3)}_qa.png"  # 檔名
    im_qa.save(os.path.join(orign_path, filename_qa))  # 路徑
    print(f"{filename_qa} 儲存完成")  # 打印
    time.sleep(1)  # 停滯 1 秒

    # 更新
    ct += 1  # 計數器

    # 下一題
    pyautogui.moveTo(408, 374)  # 移動滑鼠
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    time.sleep(1)  # 停滯 1 秒
    pyautogui.moveTo(490, 634)  # 移動滑鼠
    pyautogui.mouseDown()
    pyautogui.mouseUp()
    time.sleep(1)  # 停滯 1 秒


# pyautogui.displayMousePosition()


"""QA: 290, 145->1006, 705
Q: 290, 173->1006, 331

A: 408, 374
B: 408, 420
C: 408, 468
D: 408, 528

Y: 490, 634
N: 766, 634"""

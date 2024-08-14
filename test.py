import cv2
import pytesseract
from PIL import Image

img = cv2.imread("iqtest_q_010_2560x1600.png", cv2.IMREAD_UNCHANGED)  # 開啟圖片
img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)  # 因為是 jpg，要轉換顏色為 BGRA
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # 新增 gray 變數為轉換成灰階的圖片

h = img.shape[0]  # 取得圖片高度
w = img.shape[1]  # 取得圖片寬度

# 依序取出圖片中每個像素
for x in range(w):
    for y in range(h):
        if gray[y, x] > 120:
            img[y, x, 3] = 0
            # 如果該像素的灰階度大於 200，調整該像素的透明度
            # 使用 255 - gray[y, x] 可以將一些邊緣的像素變成半透明，避免太過鋸齒的邊緣

cv2.imwrite("oxxostudio.png", img)  # 存檔儲存為 png
cv2.waitKey(0)  # 按下任意鍵停止
cv2.destroyAllWindows()


img = Image.open("oxxostudio.png")

# 使用 pytesseract 來辨識文字
text = pytesseract.image_to_string(
    img, lang="chi_tra+chi_sim+eng"
)  # 'chi_sim' 用於簡體中文，'chi_tra' 用於繁體中文

# 打印識別的文字
print(text)  # 打開圖片

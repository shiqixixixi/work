import cv2
import pytesseract
import pandas as pd

# 定义图片路径和文件名
img_path = 'food.jpg'

# 读取图片信息
img = cv2.imread(img_path)

# 使用 OpenCV 提供的方法来检测表格
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]
sorted_ctrs = sorted(contours, key=lambda ctr: cv2.boundingRect(ctr)[0])

# 对单元格中的文字进行分列和分行
cells = {}
for i, ctr in enumerate(sorted_ctrs):
    x, y, w, h = cv2.boundingRect(ctr)
    if h > 15 and w > 15:
        roi = img[y:y+h, x:x+w]
        cells[i] = pytesseract.image_to_string(roi)

# 使用 Pandas 的 DataFrame 将表格中的数据存储为二维数组
df = pd.DataFrame(columns=["菜名", "价格"])
keys = list(cells.keys())
for i in range(len(keys) // 2):
    df.loc[i] = [cells[keys[i]], cells[keys[i + len(keys) // 2]]]

# 将数据存储到 Excel 文件中
with pd.ExcelWriter('data.xlsx') as writer:
    df.to_excel(writer, sheet_name='Sheet1', index=False)

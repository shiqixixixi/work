import cv2
import pytesseract
import re
import pandas as pd

# 读取菜单图片，进行预处理
img = cv2.imread('food.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# 文字识别
text = pytesseract.image_to_string(thresh, lang='chi_sim')

# 判断菜名和价格
menu_items = []
item_name = ''
item_price = ''
for line in text.split('\n'):
    line = line.strip()
    if not line:
        continue
    if re.search(r'^[\d\.]+$', line):
        item_price = line
    else:
        if item_name and item_price:
            menu_items.append((item_name, item_price))
        item_name = line
        item_price = ''

# 保存到 Excel 文件
df = pd.DataFrame(menu_items, columns=['菜名', '价格'])
df.to_excel('menu.xlsx', index=False)
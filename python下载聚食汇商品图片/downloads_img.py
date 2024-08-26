# 导入所需的模块
import pandas as pd
import requests
import os
import zipfile
from bs4 import BeautifulSoup
import glob
import tkinter as tk
from tkinter import filedialog
import shutil
# 获取当前工作目录路径
current_dir = os.getcwd()

# 查找当前目录下所有Excel文件
excel_files = glob.glob(os.path.join(current_dir, "*.xlsx"))

# 如果没有找到Excel文件，输出提示信息并结束程序
if not excel_files:
    print("当前目录下没有Excel文件！")
    exit()

# 让用户选择一个文件
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(title="选择要打开的Excel文件", filetypes=[("Excel文件", "*.xlsx")])

# 如果用户没有选择文件，结束程序
if not file_path:
    print("没有选择文件！")
    exit()

# 读取用户选择的Excel文件
# 读取excel文件，假设文件名为data.xlsx
#df = pd.read_excel("data.xlsx")

df = pd.read_excel(file_path)

# 获取第一列和第二列的内容，假设第一列是搜索的关键词，第二列是保存的文件名
keywords = df['名称'] 
imgname =df['编号'] 
#dm = df['所属大类'] 
dm = df.iloc[0,5]

path = str(dm)

# 创建一个文件夹来保存图片，假设文件夹名为images，如果不存在择创建 反之跳过
image_file = "images"
if not os.path.exists(image_file):
    os.makedirs(image_file)
else:
    print(f"{image_file}文件夹已经存在，已直接使用。")

if os.path.exists(f'{image_file}/{path}'):  # 判断文件夹是否存在
    for filename in os.listdir(f'{image_file}/{path}'):  # 清空文件夹中的内容
        file_path = os.path.join(f'{image_file}/{path}', filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
else:
    os.makedirs(f'{image_file}/{path}')  # 创建文件夹

# 遍历每个关键词，搜索图片并下载保存到文件夹中
for i, keyword in enumerate(keywords):
    # 构造Bing图片搜索的网址，假设每个关键词只下载第一张图片
    url = f"https://cn.bing.com/images/search?q={keyword}&first=1"
    #url = f"https://cn.bing.com/images/search?q={keyword}&first=1&qft=+filterui:imagesize-custom_1024_768"
    #url = f"https://www.bing.com/images/search?q={keyword}&first=1"
    response = requests.get(url)
    # 判断请求是否成功
    if response.status_code == 200:
        # 解析网页的源代码，提取图片的网址
        soup = BeautifulSoup(response.text, "html.parser")
        img_url = soup.find("img", class_="mimg").get("src")
        # 发送请求获取图片的二进制数据
        img_response = requests.get(img_url)
        # 判断请求是否成功
        if img_response.status_code == 200:
            # 获取图片的格式，假设是jpg或png
            ext = img_url.split(".")[-1]
            # 构造图片的文件名，假设是从imgname列表中获取，并加上扩展名
            filename = f"{image_file}/{path}/{'{:05d}'.format(imgname[i])}.jpg"
            #filename = f"images/{imgname[i]}.jpg"
            #filename = f"images/{imgname[i]}.{ext}"
            # 打开一个文件并写入图片数据
            with open(filename, "wb") as f:
                f.write(img_response.content)
            # 打印提示信息
            print(f"Downloaded and saved {img_url} as {filename}")
        else:
            # 打印错误信息
            print(f"Failed to download {img_url}")
    else:
        # 打印错误信息
        print(f"Failed to access {url}")

#压缩图片拓展名为"*.zip"
def get_jpg_files(path):
    jpg_files = []
    for root, dirs, files in os.walk(f'{image_file}/{path}'):
        for file in files:
            if file.endswith('.jpg'):
                jpg_files.append(os.path.join(root, file))
    return jpg_files

# 压缩文件为zip格式
def compress_to_zip(file_paths, zip_file):
    with zipfile.ZipFile(zip_file, 'w') as zip:
        for file in file_paths:
            zip.write(file, os.path.basename(file))

# 调用函数获取图片文件路径列表
jpg_files = get_jpg_files(path)

# 将所有jpg文件压缩为zip文件
zip_file = f'{image_file}/{path}.zip'
compress_to_zip(jpg_files, zip_file)
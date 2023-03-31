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
keywords = df.iloc[:,0]
imgname = df.iloc[:,2]
dm = df.iloc[0,1] 
path = str(dm)
# 创建一个文件夹来保存图片，假设文件夹名为images
#os.mkdir("images")

if os.path.exists(path):  # 判断文件夹是否存在
    for filename in os.listdir(path):  # 清空文件夹中的内容
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
else:
    os.makedirs(path)  # 创建文件夹

# 遍历每个关键词，搜索图片并下载保存到文件夹中
for i, keyword in enumerate(keywords):
    # 构造Bing图片搜索的网址，假设每个关键词只下载第一张图片
    #url = f"https://cn.bing.com/images/search?q={keyword}&first=1"
    url = f"https://cn.bing.com/images/search?q={keyword}&first=1&qft=+filterui:imagesize-custom_1024_768"
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
            filename = f"{path}/{(imgname[i])}.jpg"
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

# 设置源文件夹的路径
source_dir = f'{path}/'

# 设置目标文件夹的路径
target_dir = f'{path}/'

# 分割数量
split_num = 50

# 遍历源文件夹中的文件
for i, filename in enumerate(os.listdir(source_dir)):
    # 获取文件的完整路径
    filepath = os.path.join(source_dir, filename)
    
    # 设置目标文件夹的名称
    target_subdir_name = f'folder_{i // split_num + 1}'
    target_subdir = os.path.join(target_dir, target_subdir_name)
    
    # 如果目标文件夹不存在，就创建它
    if not os.path.exists(target_subdir):
        os.makedirs(target_subdir)
    
    # 将文件复制到目标文件夹
    shutil.copy2(filepath, target_subdir)


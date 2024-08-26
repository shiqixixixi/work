import pandas as pd
import tkinter as tk
from tkinter import filedialog

def split_excel():
    root = tk.Tk()
    root.withdraw()  # 隐藏主窗口

    file_path = filedialog.askopenfilename()  # 弹出文件选择窗口

    df = pd.read_excel(file_path, dtype=object)  # 确保读取时保留所有数据的原始格式

    # 定义要删除的无效列
    #invalid_columns = ["大客户", "企业名称", "合同号", "联系人", "归属门店账号", "开卡门店", "导购员", "赊账额度", "是否关注公众号", "是否绑定企微"]
    invalid_columns = ["导购员", "赊账额度", "是否关注公众号", "是否绑定企微"]
    df = df.drop(columns=invalid_columns)

    # 检查并交换"余额（必填）"和"储值赠送部分"列的位置
    if '余额（必填）' in df.columns and '储值赠送部分' in df.columns:
        balance_column = df['余额（必填）']
        gift_column = df['储值赠送部分']
        for index, (balance_value, gift_value) in enumerate(zip(balance_column, gift_column)):
            if pd.to_numeric(gift_value, errors='coerce') > pd.to_numeric(balance_value, errors='coerce'):
                df.loc[index, '余额（必填）'], df.loc[index, '储值赠送部分'] = gift_value, balance_value

    num_splits = len(df) // 999 + 1
    for i in range(num_splits):
        start = i * 999
        end = min((i + 1) * 999, len(df))
        split_df = df.iloc[start:end]  # 使用 iloc 方法按行索引切片，保持原有结构
        split_df.to_excel(f"split_{i + 1}.xlsx", index=False, engine='openpyxl')  # 使用 openpyxl 引擎以保持格式

split_excel()
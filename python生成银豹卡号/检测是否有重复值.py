import os
import pandas as pd

# 获取当前目录下所有的 Excel 文件
excel_files = [filename for filename in os.listdir('.')
               if filename.endswith('.xlsx') or filename.endswith('.xls')]

# 列出文件名并让用户选择需要读取的文件
print('请选择要读取的 Excel 文件：')
for i, filename in enumerate(excel_files):
    print(f'{i + 1}. {filename}')

file_index = int(input()) - 1
selected_file = excel_files[file_index]

# 读取选择的 Excel 文件
df = pd.read_excel(selected_file)

# 列出数据框中的列并让用户选择感兴趣的列
print('请选择要检查的列（输入数字，多个列用空格隔开）：')
for i, colname in enumerate(df.columns):
    print(f'{i + 1}. {colname}')

selected_cols = input().split()
selected_cols = [int(i) - 1 for i in selected_cols]

# 检查选定列是否有重复值
duplicates = []
for col_idx in selected_cols:
    colname = df.columns[col_idx]
    if df[colname].duplicated().any():
        duplicates.append(colname)

# 将重复值导出到另一个文本文件
if duplicates:
    with open('duplicates.txt', 'w') as f:
        f.write('\n'.join(duplicates))
else:
    print('没有发现重复值。')


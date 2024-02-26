import random
from datetime import datetime
import pandas as pd

quantity = input("请输入要生成的卡号数量（如果不输入默认为1000）：")
if quantity:
    try:
        quantity = int(quantity)
    except ValueError:
        quantity = 1000
else:
    quantity = 1000
#quantity = 1000 #定义的卡号数量

def generate_random_numbers(n):
    result = set()
    while len(result) < n:
        num = str(random.randint(46,57)) + ''.join([str(random.randint(0,9)) for _ in range(17)])
        result.add(num)
    return list(result)

random_numbers = generate_random_numbers(quantity) #卡号数量
filename = datetime.now().strftime('%Y' + '年' + '%m' + '月' + '%d' + '日' + '%H' + '时' + '%M' + '分' + '%S' + '秒') + str(quantity) + ('张卡号') + '.xlsx'
df = pd.DataFrame(random_numbers, columns=['卡号'])
df.to_excel(filename, index=False)
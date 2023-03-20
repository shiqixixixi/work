import random
import time
import xlsxwriter

quantity = 1000 #定义的卡号数量

def generate_random_number():
    first_two_digits = random.randint(46, 57)  # 前两位数字在46到57之间的随机整数
    other_digits = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 17)])  # 剩余数字为0~9的随机整数
    random_number = str(first_two_digits) + other_digits
    return random_number

file_name = time.strftime('%Y' + '年' + '%m' + '月' + '%d' + '日' + '%H' + '时' + '%M' + '分' + '%S' + '秒') + str(quantity) + ('张卡号') + '.xlsx'
#filename = datetime.now().strftime('%Y' + '年' + '%m' + '月' + '%d' + '日' + '%H' + '时' + '%M' + '分' + '%S' + '秒') + str(quantity) + ('张卡号') + '.xlsx'
random_numbers = set()

while len(random_numbers) < quantity: #sc
    random_numbers.add(generate_random_number())

while True:
    if len(random_numbers) != len(set(random_numbers)):
        random_numbers = set()
        while len(random_numbers) < quantity: #chkdsk
            random_numbers.add(generate_random_number())
    else:
        break

workbook = xlsxwriter.Workbook(file_name)
worksheet = workbook.add_worksheet()

for i, number in enumerate(random_numbers):
    worksheet.write(i, 0, number)

workbook.close()
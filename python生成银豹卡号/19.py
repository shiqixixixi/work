import random
import time

def generate_random_number():
    first_two_digits = random.randint(46, 57)  # 前两位数字在46到57之间的随机整数
    other_digits = ''.join(["{}".format(random.randint(0, 9)) for num in range(0, 17)])  # 剩余数字为0~9的随机整数
    random_number = str(first_two_digits) + other_digits
    return random_number

random_numbers = set()  # 使用集合存储不重复的随机数
while len(random_numbers) < 1000:
    random_numbers.add(generate_random_number())

file_name = time.strftime("%Y%m%d-%H%M%S") + ".txt"

with open(file_name, 'w') as file:
    for num in random_numbers:
        file.write(num + '\n')
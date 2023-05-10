import openpyxl

# 创建Excel文件对象
workbook = openpyxl.Workbook()

# 获取活动工作表
worksheet = workbook.active

# 添加列名
columns = ['编号', '助记码', '名称', '别名', '品牌', '所属小类', '所属大类', '商品类型', '单位', '启用', '启用做法', '商品做法', '商品做法类型', '套餐商品', '比例折扣', '时价商品', '临时商品', '即时录入数量', '称重', '允许使用代金券', '允许使用卡余额', '特色商品', '下载点菜宝', '收服务费', '允许积分', '计入最低消费', '前台排序', '参考价1', '会员价1']
worksheet.append(columns)

# 保存Excel文件
workbook.save('商品信息.xlsx')

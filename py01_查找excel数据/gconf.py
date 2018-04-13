#encoding=utf-8

# field 是excel中的列
field = '业务系统'

# input_excel 是待查找的表格
input_excel = 'test.xls'
# input_excel = 'test1.xlsx'

# file_name 是要读入待查找的数据
file_name = 'ip.txt'

# output_excel 存放的是查找到的信息 
output_excel = 'output.xls'

# output 存放的是没查找的信息
no_found = 'no_found.txt'

# all_sheet = True, 表示输出查找到的所有sheet的数据
all_sheet = False

# 当all_sheet为False时，sheet_list才生效, 这里可以选择需要输出哪几个sheet的数据;
sheet_list = ['sheet1', 'sheet2', 'sheetX']

# 将不同sheet的数据合并到同一个表中,默认不合并,如需合并不同的sheet,要将merge值修改为True
merge = True

# 选择需要输出的列,以逗号分隔; 当 merge=True 时才可使用, 列的顺序为excel中显示的顺序
outputfiled = ['第1列','第5列','第9列','第10列']

# 输出合并后的表格,当 当 merge=True 时才有效
mergeoupt_excel = 'merge_output.xls'

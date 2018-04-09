#encoding=utf-8

# field 是excel中的字段
field = '业务系统名称'

# excelFile 是待查找的表格
# excelFile = 'test1.xlsx'
excelFile = 'test.xls'

# file_name 是要读入待查找的数据
file_name = 'ip.txt'

# output_excel 存放的是查找到的信息 
output_excel = 'output.xls'

# output 存放的是没查找的信息
no_found = 'no_found.txt'

# 将不同sheet的数据合并到同一个表中,默认不合并,如需合并要将merge值修改为True
merge = False

# 选择需要输出的字段,以逗号分隔; 当 merge=True 时才可使用, 字段的顺序为excel中显示的顺序
outputfiled = ['名称','代理商','产地', '价格']

# 输出合并后的表格,当 当 merge=True 时才有效
mergeoupt_excel = 'merge_output.xls'
